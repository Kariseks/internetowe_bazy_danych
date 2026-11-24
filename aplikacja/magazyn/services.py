"""Asortyment i ruchy magazynowe sklepu."""
from collections import defaultdict
from datetime import datetime, time, timedelta
from decimal import Decimal, ROUND_HALF_UP
from types import SimpleNamespace

from django.db import IntegrityError, transaction
from django.db.models import OuterRef, Subquery, Sum
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.utils.translation import gettext as _

from rezerwacje.models import PozycjaRezerwacji, Rezerwacja
from .models import (CenaProduktu, Dostawa, KorektaStanu, PlanDostawy, PozycjaDostawy,
                     PozycjaSprzedazy, Produkt, Sprzedaz, Ubytek)


class ProduktOdrzucony(Exception):
    pass


class BrakNaStanie(Exception):
    pass


class DostawaOdrzucona(Exception):
    pass


def grosze(kwota):
    return kwota.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def produkty(dzien=None):
    ceny = CenaProduktu.objects.filter(produkt_id=OuterRef('pk'), obowiazuje_od__lte=dzien or timezone.localdate())
    return Produkt.objects.annotate(cena_za_kg=Subquery(ceny.order_by('-obowiazuje_od').values('cena_za_kg')[:1])).order_by('nazwa', 'odmiana')


def produkt(produkt_id):
    p = produkty().filter(pk=produkt_id).first()
    if p:
        p.ceny = CenaProduktu.objects.filter(produkt=p).order_by('-obowiazuje_od')
    return p


def dodaj_produkt(nazwa, odmiana, standardowa_ilosc_kg, w_ofercie, cena_za_kg, obowiazuje_od, ilosc_na_lade_kg=0, jednostka="kg"):
    try:
        with transaction.atomic():
            p = Produkt(jednostka=jednostka, nazwa=nazwa, odmiana=odmiana, standardowa_ilosc_kg=standardowa_ilosc_kg,
                                       w_ofercie=w_ofercie, ilosc_na_lade_kg=ilosc_na_lade_kg)
            p.sprawdz_ilosc(standardowa_ilosc_kg, ProduktOdrzucony)
            p.sprawdz_ilosc(ilosc_na_lade_kg, ProduktOdrzucony)
            p.save()
            zmien_cene(p.pk, cena_za_kg, obowiazuje_od)
            return p
    except IntegrityError as blad:
        raise ProduktOdrzucony(_('Sprawdź nazwę, odmianę i podane ilości produktu.')) from blad


@transaction.atomic
def zmien_produkt(produkt_id, nazwa, odmiana, standardowa_ilosc_kg, w_ofercie, ilosc_na_lade_kg=None):
    p = Produkt.objects.select_for_update().get(pk=produkt_id)
    lada = p.ilosc_na_lade_kg if ilosc_na_lade_kg is None else ilosc_na_lade_kg
    p.sprawdz_ilosc(lada, ProduktOdrzucony)
    p.sprawdz_ilosc(standardowa_ilosc_kg, ProduktOdrzucony)
    for plan in PlanDostawy.objects.filter(produkt=p, dzien__gt=timezone.localdate()):
        zajete = rezerwowane(plan.dzien).get(p.pk, 0)
        if plan.ilosc_kg < lada + zajete:
            raise ProduktOdrzucony(_('Ilość na ladę narusza zapisany plan dostawy.'))
    try:
        with transaction.atomic():
            Produkt.objects.filter(pk=p.pk).update(nazwa=nazwa, odmiana=odmiana, standardowa_ilosc_kg=standardowa_ilosc_kg,
                                                   w_ofercie=w_ofercie, ilosc_na_lade_kg=lada)
    except IntegrityError as blad:
        raise ProduktOdrzucony(_('Sprawdź nazwę, odmianę i podane ilości produktu.')) from blad


def zmien_cene(produkt_id, cena_za_kg, obowiazuje_od):
    try:
        with transaction.atomic():
            CenaProduktu.objects.create(produkt_id=produkt_id, cena_za_kg=cena_za_kg, obowiazuje_od=obowiazuje_od)
    except IntegrityError as blad:
        raise ProduktOdrzucony(_('Podaj dodatnią cenę i dzień bez innej zmiany ceny.')) from blad


def sumy(wiersze, pole):
    return dict(wiersze.order_by().values('produkt_id').annotate(s=Sum(pole)).values_list('produkt_id', 's'))


def stany(ids):
    razem = defaultdict(Decimal)
    for model, pole, znak in [(PozycjaDostawy, 'ilosc_kg', 1), (PozycjaSprzedazy, 'masa_kg', -1),
                              (Ubytek, 'masa_kg', -1), (KorektaStanu, 'roznica_kg', 1)]:
        for pid, masa in sumy(model.objects.filter(produkt_id__in=ids), pole).items():
            razem[pid] += znak * masa
    return razem


def stan_produktow():
    oferta = list(produkty().filter(w_ofercie=True))
    stan = stany([p.pk for p in oferta])
    return [SimpleNamespace(produkt=p, cena_za_kg=p.cena_za_kg, stan_kg=stan[p.pk]) for p in oferta]


def rezerwowane(dzien, pomin=None, niewydane=False):
    pozycje = PozycjaRezerwacji.objects.filter(rezerwacja__dzien_odbioru=dzien).exclude(rezerwacja__stan='anulowana')
    if pomin is not None:
        pozycje = pozycje.exclude(rezerwacja_id=pomin)
    if niewydane:
        pozycje = pozycje.filter(rezerwacja__stan__in=('zlozona', 'przygotowana'))
        return sumy(pozycje, Coalesce('masa_odwazona_kg', 'ilosc_kg'))
    return sumy(pozycje, 'ilosc_kg')


def plan_na_dzien(dzien, pomin=None, asortyment=None):
    plany = dict(PlanDostawy.objects.filter(dzien=dzien).values_list('produkt_id', 'ilosc_kg'))
    zajete = rezerwowane(dzien, pomin)
    if asortyment is None:
        asortyment = produkty().filter(w_ofercie=True)
    wynik = []
    for p in asortyment:
        plan = plany.get(p.pk, p.standardowa_ilosc_kg)
        zajeto = zajete.get(p.pk, Decimal(0))
        wynik.append(SimpleNamespace(produkt=p, cena_za_kg=p.cena_za_kg, dzien=dzien, plan_kg=plan,
                                     ilosc_na_lade_kg=p.ilosc_na_lade_kg, zarezerwowano_kg=zajeto,
                                     dostepne_kg=max(0, plan - p.ilosc_na_lade_kg - zajeto)))
    return wynik


def dostawa_na_dzien(dzien):
    dostawa = Dostawa.objects.filter(dzien=dzien).first()
    if not dostawa:
        return None
    masy = dict(PozycjaDostawy.objects.filter(dostawa=dostawa).values_list('produkt_id', 'ilosc_kg'))
    dostawa.pozycje = plan_na_dzien(dzien, asortyment=produkty(dzien).filter(pk__in=masy))
    for w in dostawa.pozycje:
        w.dostarczono_kg = masy[w.produkt.pk]
        w.roznica_kg = w.dostarczono_kg - w.plan_kg
        w.za_malo = w.dostarczono_kg < w.zarezerwowano_kg
    return dostawa


def blokuj_produkty(ids):
    return {p.pk: p for p in Produkt.objects.select_for_update().filter(pk__in=ids).order_by('pk')}


def zarejestruj_dostawe(dzien, pozycje, kto):
    try:
        with transaction.atomic():
            wybrane = blokuj_produkty([pid for pid, masa in pozycje])
            dostawa = Dostawa.objects.create(dzien=dzien, zarejestrowano=timezone.now(), zarejestrowal=kto)
            for pid, masa in pozycje:
                if pid not in wybrane or masa < 0:
                    raise DostawaOdrzucona(_('Sprawdź produkt i masę dostawy.'))
                wybrane[pid].sprawdz_ilosc(masa, DostawaOdrzucona)
                PlanDostawy.objects.get_or_create(produkt_id=pid, dzien=dzien, defaults={'ilosc_kg': wybrane[pid].standardowa_ilosc_kg})
                PozycjaDostawy.objects.create(dostawa=dostawa, produkt_id=pid, ilosc_kg=masa)
            return dostawa
    except IntegrityError as blad:
        raise DostawaOdrzucona(_('Dostawa na ten dzień została już zapisana lub zawiera powtórzony produkt.')) from blad


@transaction.atomic
def zarejestruj_sprzedaz(pozycje, kto, rezerwacja=None):
    ids = [pid for pid, masa in pozycje]
    if not ids or len(set(ids)) != len(ids):
        raise BrakNaStanie(_('Wybierz produkty do sprzedaży.'))
    blokuj_produkty(ids)
    dzien = timezone.localdate()
    cennik = {p.pk: p for p in produkty(dzien).filter(pk__in=ids)}
    stan = stany(ids)
    chronione = rezerwowane(dzien, pomin=rezerwacja.pk if rezerwacja else None, niewydane=True)
    sprzedaz = Sprzedaz.objects.create(data_czas=timezone.now(), sprzedawca=kto, rezerwacja=rezerwacja)
    sprzedaz.suma = Decimal(0)
    for pid, masa in pozycje:
        p = cennik.get(pid)
        if p is None or p.cena_za_kg is None or (not p.w_ofercie and not rezerwacja):
            raise BrakNaStanie(_('Produkt nie ma dostępnej ceny sprzedaży.'))
        dostepne = stan[pid] if rezerwacja else max(0, stan[pid] - chronione.get(pid, 0))
        p.sprawdz_ilosc(masa, BrakNaStanie)
        if masa <= 0 or masa > dostepne:
            raise BrakNaStanie(_('%(produkt)s: dostępne %(kg)s %(unit)s.') % {'produkt': p, 'kg': dostepne, 'unit': p.symbol})
        PozycjaSprzedazy.objects.create(sprzedaz=sprzedaz, produkt=p, cena_za_kg=p.cena_za_kg, masa_kg=masa)
        sprzedaz.suma += grosze(masa * p.cena_za_kg)
    return sprzedaz


@transaction.atomic
def zarejestruj_ubytek(produkt_id, masa_kg, kto):
    produkt = blokuj_produkty([produkt_id])[produkt_id]
    produkt.sprawdz_ilosc(masa_kg, BrakNaStanie)
    stan = stany([produkt_id])[produkt_id]
    if not 0 < masa_kg <= stan:
        raise BrakNaStanie(_('Stan produktu: %(kg)s %(unit)s.') % {'kg': stan, 'unit': produkt.symbol})
    Ubytek.objects.create(produkt_id=produkt_id, masa_kg=masa_kg, data_czas=timezone.now(), zarejestrowal=kto)


@transaction.atomic
def skoryguj_stan(produkt_id, masa_kg, przyczyna, kto):
    produkt = blokuj_produkty([produkt_id])[produkt_id]
    produkt.sprawdz_ilosc(masa_kg, BrakNaStanie)
    if masa_kg < 0 or not przyczyna.strip():
        raise BrakNaStanie(_('Podaj zważoną masę i przyczynę korekty.'))
    roznica = masa_kg - stany([produkt_id])[produkt_id]
    if roznica:
        KorektaStanu.objects.create(produkt_id=produkt_id, roznica_kg=roznica, przyczyna=przyczyna,
                                    data_czas=timezone.now(), zarejestrowal=kto)


def okres(od, do):
    return {'data_czas__gte': timezone.make_aware(datetime.combine(od, time.min)),
            'data_czas__lt': timezone.make_aware(datetime.combine(do + timedelta(days=1), time.min))}


def historia_sprzedazy(od, do):
    sprzedaze = list(Sprzedaz.objects.filter(**okres(od, do)).select_related('sprzedawca').order_by('-data_czas', '-pk'))
    linie = defaultdict(list)
    for p in PozycjaSprzedazy.objects.filter(sprzedaz__in=sprzedaze).select_related('produkt').order_by('pk'):
        p.wartosc = grosze(p.masa_kg * p.cena_za_kg)
        linie[p.sprzedaz_id].append(p)
    for s in sprzedaze:
        s.pozycje = linie[s.pk]
        s.suma = sum(p.wartosc for p in s.pozycje)
    return sprzedaze


def zestawienia(od, do):
    sprzedane = {}
    for s in historia_sprzedazy(od, do):
        for p in s.pozycje:
            w = sprzedane.setdefault(p.produkt_id, SimpleNamespace(produkt=p.produkt, masa_kg=0, wartosc=0))
            w.masa_kg += p.masa_kg
            w.wartosc += p.wartosc
    ubytki = sumy(Ubytek.objects.filter(**okres(od, do)), 'masa_kg')
    roznice = []
    for dzien in Dostawa.objects.filter(dzien__range=(od, do)).order_by('dzien').values_list('dzien', flat=True):
        roznice.extend(w for w in dostawa_na_dzien(dzien).pozycje if w.roznica_kg)
    from rezerwacje.services import dane_rezerwacji
    brak = Rezerwacja.objects.filter(stan='nieodebrana', dzien_odbioru__range=(od, do))
    return SimpleNamespace(sprzedaz=list(sprzedane.values()), roznice=roznice,
                           ubytki=[SimpleNamespace(produkt=p, masa_kg=ubytki[p.pk]) for p in Produkt.objects.filter(pk__in=ubytki)],
                           nieodebrane=SimpleNamespace(liczba=brak.count(), wartosc=sum(r.wartosc for r in dane_rezerwacji(brak))))
