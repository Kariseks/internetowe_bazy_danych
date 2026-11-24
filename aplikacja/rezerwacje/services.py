"""Rezerwacje, pule dostaw i obsługa odbioru."""
import logging
import smtplib
from datetime import datetime, time, timedelta
from decimal import Decimal
from types import SimpleNamespace

from django.db import IntegrityError, OperationalError, transaction
from django.db.models import Prefetch
from django.utils import timezone
from django.utils.translation import gettext as _

from konta import powiadomienia
from konta.models import ProfilKlienta
from magazyn import services as magazyn
from magazyn.models import Dostawa, PlanDostawy
from rozliczenia.services import uzupelnij_saldo
from .models import PozycjaRezerwacji, Rezerwacja

log = logging.getLogger(__name__)
LIMIT_KG = Decimal(20)
AKTYWNE = ('zlozona', 'przygotowana')


class RezerwacjaOdrzucona(Exception):
    pass


class PlanOdrzucony(Exception):
    pass


def termin(dzien):
    return timezone.make_aware(datetime.combine(dzien - timedelta(days=1), time(18)))


def otwarty(dzien):
    dzis = timezone.localdate()
    return dzis < dzien <= dzis + timedelta(days=7) and timezone.now() < termin(dzien)


def dane_rezerwacji(zapytanie):
    linie = PozycjaRezerwacji.objects.select_related('produkt').order_by('pk')
    rekordy = list(zapytanie.select_related('klient__uzytkownik').prefetch_related(
        Prefetch('pozycjarezerwacji_set', queryset=linie, to_attr='pozycje')))
    ceny = {}
    profile = {}
    for r in rekordy:
        dzien = min(timezone.localdate(), r.dzien_odbioru)
        if dzien not in ceny:
            ceny[dzien] = dict(magazyn.produkty(dzien).values_list('pk', 'cena_za_kg'))
        if r.klient_id not in profile:
            profile[r.klient_id] = uzupelnij_saldo(r.klient)
        r.klient = profile[r.klient_id]
        r.termin = termin(r.dzien_odbioru)
        r.mozna_zmienic = r.stan == 'zlozona' and timezone.now() < r.termin
        r.laczna_masa = sum(p.ilosc_kg for p in r.pozycje if p.produkt.jednostka == "kg")
        r.liczba_sztuk = sum(p.ilosc_kg for p in r.pozycje if p.produkt.jednostka == "szt")
        r.wartosc = sum(magazyn.grosze(p.ilosc_kg * ceny[dzien][p.produkt_id]) for p in r.pozycje)
    return rekordy


def rezerwacje_na_dzien(dzien):
    return dane_rezerwacji(Rezerwacja.objects.filter(dzien_odbioru=dzien).order_by('zlozono', 'pk'))


def rezerwacja(rezerwacja_id):
    return next(iter(dane_rezerwacji(Rezerwacja.objects.filter(pk=rezerwacja_id))), None)


def rezerwacje_klienta(uzytkownik):
    return dane_rezerwacji(Rezerwacja.objects.filter(klient_id=uzytkownik.pk).order_by('-dzien_odbioru', '-pk'))


def rezerwacja_klienta(uzytkownik, rezerwacja_id):
    return next(iter(dane_rezerwacji(Rezerwacja.objects.filter(klient_id=uzytkownik.pk, pk=rezerwacja_id))), None)


def katalog():
    oferta = list(magazyn.produkty().filter(w_ofercie=True, cena_za_kg__isnull=False))
    dni = []
    wiersze = {p.pk: SimpleNamespace(produkt=p, cena_za_kg=p.cena_za_kg, komorki=[]) for p in oferta}
    for i in range(1, 8):
        dzien = timezone.localdate() + timedelta(days=i)
        zamkniety = not otwarty(dzien)
        dni.append(SimpleNamespace(dzien=dzien, zamkniety=zamkniety))
        for komorka in magazyn.plan_na_dzien(dzien, asortyment=oferta):
            komorka.zamkniety = zamkniety
            wiersze[komorka.produkt.pk].komorki.append(komorka)
    return SimpleNamespace(wiersze=list(wiersze.values()), dni=dni)


def plan_tygodnia():
    return katalog()


def oferta_na_dzien(dzien, rezerwacja_id=None):
    if not timezone.localdate() < dzien <= timezone.localdate() + timedelta(days=7):
        return []
    return [w for w in magazyn.plan_na_dzien(dzien, rezerwacja_id) if w.cena_za_kg is not None]


def przeszkoda(uzytkownik, dzien):
    wynik = SimpleNamespace(powod=None, rezerwacja=None, zaleglosc=None)
    if not otwarty(dzien):
        wynik.powod = 'zamkniete'
        return wynik
    profil = ProfilKlienta.objects.filter(pk=uzytkownik.pk).first()
    if not profil or not profil.identyfikator_karty:
        wynik.powod = 'karta'
    elif uzupelnij_saldo(profil).zablokowany:
        wynik.powod, wynik.zaleglosc = 'zaleglosc', profil.zaleglosc
    else:
        wynik.rezerwacja = Rezerwacja.objects.filter(klient=profil, dzien_odbioru=dzien, stan__in=AKTYWNE).first()
        if not wynik.rezerwacja:
            return None
        wynik.rezerwacja = rezerwacja(wynik.rezerwacja.pk)
        wynik.powod = 'istnieje'
    return wynik


def _zapisz_pozycje(uzytkownik, dzien, pozycje, rezerwacja_id=None):
    zdarzenie = 'zmieniona' if rezerwacja_id else 'zlozona'
    try:
        with transaction.atomic():
            profil = ProfilKlienta.objects.select_for_update().get(pk=uzytkownik.pk)
            if not profil.uzytkownik.is_active:
                raise RezerwacjaOdrzucona(_('Konto jest nieaktywne.'))
            if rezerwacja_id:
                r = Rezerwacja.objects.select_for_update().filter(pk=rezerwacja_id, klient=profil, stan='zlozona').first()
                if not r:
                    raise RezerwacjaOdrzucona(_('Nie można zmienić tej rezerwacji.'))
                dzien = r.dzien_odbioru
            elif przeszkoda(uzytkownik, dzien):
                raise RezerwacjaOdrzucona(_('Sprawdź termin, kartę, saldo i rezerwacje na ten dzień.'))
            ids = [pid for pid, masa in pozycje]
            if not ids or len(set(ids)) != len(ids):
                raise RezerwacjaOdrzucona(_('Wybierz produkty o łącznej masie do 20 kg.'))
            produkty = magazyn.blokuj_produkty(ids)
            if sum(m for pid, m in pozycje if pid in produkty and produkty[pid].jednostka == "kg") > LIMIT_KG:
                raise RezerwacjaOdrzucona(_('Wybierz produkty o łącznej masie do 20 kg.'))
            if not otwarty(dzien):
                raise RezerwacjaOdrzucona(_('Minął termin rezerwacji.'))
            oferta = {w.produkt.pk: w for w in oferta_na_dzien(dzien, rezerwacja_id)}
            for pid, masa in pozycje:
                w = oferta.get(pid)
                if not w:
                    raise RezerwacjaOdrzucona(_('Produkt jest niedostępny.'))
                w.produkt.sprawdz_ilosc(masa, RezerwacjaOdrzucona)
                if masa <= 0 or masa > w.dostepne_kg or masa != Decimal(masa).quantize(Decimal('0.1')):
                    raise RezerwacjaOdrzucona(_('Dostępne: %(kg)s %(unit)s.') % {'kg': w.dostepne_kg, 'unit': w.produkt.symbol})
                PlanDostawy.objects.get_or_create(produkt_id=pid, dzien=dzien,
                                                  defaults={'ilosc_kg': w.plan_kg})
            if rezerwacja_id:
                PozycjaRezerwacji.objects.filter(rezerwacja=r).delete()
                r.zmieniono = timezone.now()
                r.save(update_fields=['zmieniono'])
            else:
                r = Rezerwacja.objects.create(klient=profil, dzien_odbioru=dzien, stan='zlozona',
                                              zlozono=timezone.now(), zmieniono=timezone.now())
            PozycjaRezerwacji.objects.bulk_create([
                PozycjaRezerwacji(rezerwacja=r, produkt_id=pid, ilosc_kg=masa) for pid, masa in pozycje
            ])
    except OperationalError as blad:
        if blad.args[0] not in (1205, 1213):
            raise
        raise RezerwacjaOdrzucona(_('Inny zapis trwa. Spróbuj ponownie.')) from blad
    except IntegrityError as blad:
        raise RezerwacjaOdrzucona(_('Nie udało się zapisać rezerwacji. Sprawdź dostępność.')) from blad
    wynik = rezerwacja(r.pk)
    _powiadom(powiadomienia.rezerwacja, wynik, zdarzenie)
    return wynik


def _powiadom(wyslij, r, *args):
    try:
        wyslij(r, *args)
    except (smtplib.SMTPException, OSError):
        log.exception('Nie wysłano wiadomości dotyczącej rezerwacji %s', r.pk)


def zloz_rezerwacje(uzytkownik, dzien, pozycje):
    return _zapisz_pozycje(uzytkownik, dzien, pozycje)


def zmien_rezerwacje(uzytkownik, rezerwacja_id, pozycje):
    return _zapisz_pozycje(uzytkownik, None, pozycje, rezerwacja_id)


def _ustaw_stan(r, stan):
    r.stan, r.zmieniono = stan, timezone.now()
    r.save(update_fields=['stan', 'zmieniono', 'oplata_za_nieodebranie'])


def anuluj_rezerwacje(uzytkownik, rezerwacja_id):
    with transaction.atomic():
        r = Rezerwacja.objects.select_for_update().filter(pk=rezerwacja_id, klient_id=uzytkownik.pk, stan='zlozona').first()
        if not r or not otwarty(r.dzien_odbioru):
            raise RezerwacjaOdrzucona(_('Nie można anulować tej rezerwacji.'))
        _ustaw_stan(r, 'anulowana')
    _powiadom(powiadomienia.rezerwacja, rezerwacja(r.pk), 'anulowana')


@transaction.atomic
def ustaw_plan(produkt_id, dzien, ilosc_kg):
    produkt = magazyn.blokuj_produkty([produkt_id]).get(produkt_id)
    if not produkt or not otwarty(dzien):
        raise PlanOdrzucony(_('Dzień jest zamknięty.'))
    produkt.sprawdz_ilosc(ilosc_kg, PlanOdrzucony)
    zajete = magazyn.rezerwowane(dzien).get(produkt_id, 0)
    if ilosc_kg < zajete + produkt.ilosc_na_lade_kg:
        raise PlanOdrzucony(_('Zarezerwowano %(kg)s %(unit)s, na ladę przeznaczono %(lada)s %(unit)s.') %
                            {'kg': zajete, 'lada': produkt.ilosc_na_lade_kg, 'unit': produkt.symbol})
    PlanDostawy.objects.update_or_create(produkt=produkt, dzien=dzien, defaults={'ilosc_kg': ilosc_kg})


def _do_obslugi(rezerwacja_id, stany):
    r = Rezerwacja.objects.select_for_update().filter(pk=rezerwacja_id, dzien_odbioru=timezone.localdate(), stan__in=stany).first()
    if not r or timezone.localtime().hour >= 18:
        raise RezerwacjaOdrzucona(_('Rezerwacja nie jest dostępna do obsługi.'))
    return r


@transaction.atomic
def przygotuj_rezerwacje(rezerwacja_id, masy, kto):
    r = _do_obslugi(rezerwacja_id, AKTYWNE)
    if not Dostawa.objects.filter(dzien=r.dzien_odbioru).exists():
        raise RezerwacjaOdrzucona(_('Najpierw zarejestruj dzisiejszą dostawę.'))
    pozycje = list(PozycjaRezerwacji.objects.filter(rezerwacja=r))
    odwazone = dict(masy)
    if set(odwazone) != {p.produkt_id for p in pozycje} or any(m < 0 for m in odwazone.values()):
        raise RezerwacjaOdrzucona(_('Podaj masę każdego zamówionego produktu.'))
    produkty = magazyn.blokuj_produkty(odwazone)
    for p in pozycje:
        produkty[p.produkt_id].sprawdz_ilosc(odwazone[p.produkt_id], RezerwacjaOdrzucona)
        p.masa_odwazona_kg = odwazone[p.produkt_id]
    PozycjaRezerwacji.objects.bulk_update(pozycje, ['masa_odwazona_kg'])
    _ustaw_stan(r, 'przygotowana')


def podsumowanie_wydania(rezerwacja_id):
    r = rezerwacja(rezerwacja_id)
    if r is None:
        return None
    ceny = dict(magazyn.produkty(r.dzien_odbioru).values_list('pk', 'cena_za_kg'))
    for p in r.pozycje:
        p.cena_za_kg = ceny[p.produkt_id]
        p.masa_kg = p.masa_odwazona_kg or Decimal(0)
        p.wartosc = magazyn.grosze(p.masa_kg * p.cena_za_kg)
    return SimpleNamespace(rezerwacja=r, pozycje=r.pozycje, do_zaplaty=sum(p.wartosc for p in r.pozycje))


@transaction.atomic
def wydaj_rezerwacje(rezerwacja_id, kto):
    r = _do_obslugi(rezerwacja_id, ['przygotowana'])
    pozycje = list(PozycjaRezerwacji.objects.filter(rezerwacja=r, masa_odwazona_kg__gt=0).values_list('produkt_id', 'masa_odwazona_kg'))
    try:
        if pozycje:
            magazyn.zarejestruj_sprzedaz(pozycje, kto, r)
    except magazyn.BrakNaStanie as blad:
        raise RezerwacjaOdrzucona(str(blad)) from blad
    _ustaw_stan(r, 'odebrana')


def do_przypomnienia(dzien):
    wynik = dane_rezerwacji(Rezerwacja.objects.filter(dzien_odbioru=dzien, stan__in=AKTYWNE).order_by('pk'))
    for r in wynik:
        r.oplata = magazyn.grosze(r.wartosc / 10)
    return wynik


def oznacz_nieodebrane(dzien):
    teraz = timezone.localtime()
    ostatni = teraz.date() if teraz.hour >= 18 else teraz.date() - timedelta(days=1)
    ids = Rezerwacja.objects.filter(dzien_odbioru__lte=min(dzien, ostatni), stan__in=AKTYWNE).values_list('pk', 'klient_id')
    for pk, klient_id in list(ids):
        with transaction.atomic():
            ProfilKlienta.objects.select_for_update().get(pk=klient_id)
            r = Rezerwacja.objects.select_for_update().filter(pk=pk, stan__in=AKTYWNE).first()
            if not r:
                continue
            r.oplata_za_nieodebranie = magazyn.grosze(rezerwacja(pk).wartosc / 10)
            _ustaw_stan(r, 'nieodebrana')
        _powiadom(powiadomienia.oplata, rezerwacja(pk))


def wyslij_przypomnienia(dzien):
    """PU32, o 6:00 (polecenie wyslij_przypomnienia). Błąd wysyłki jednej wiadomości nie zatrzymuje pozostałych.

    Zwraca (wysłane, nieudane): liczbę wysłanych wiadomości i listę rezerwacji, do których wysłanie się nie powiodło.
    """
    wyslane, nieudane = 0, []
    for r in do_przypomnienia(dzien):
        try:
            powiadomienia.przypomnienie(r, r.oplata)
        except (smtplib.SMTPException, OSError):
            log.exception('Przypomnienie o rezerwacji %s nie zostało wysłane', r.id)
            nieudane.append(r)
        else:
            wyslane += 1
    return wyslane, nieudane
