"""Saldo klienta powstaje z naliczonych opłat i skutecznych rozliczeń."""
from types import SimpleNamespace

from django.db import transaction
from django.db.models import Q, Sum
from django.utils import timezone
from django.utils.translation import gettext as _

from konta.models import ProfilKlienta
from rezerwacje.models import Rezerwacja
from .models import RozliczenieZaleglosci


class RozliczenieOdrzucone(Exception):
    pass


def uzupelnij_saldo(profil):
    oplaty = Rezerwacja.objects.filter(klient=profil).aggregate(s=Sum('oplata_za_nieodebranie', default=0))
    wplaty = RozliczenieZaleglosci.objects.filter(klient=profil, skuteczne=True).aggregate(s=Sum('kwota', default=0))
    profil.zaleglosc = oplaty['s'] - wplaty['s']
    profil.zablokowany = profil.zaleglosc > 100
    return profil


def wyszukaj_klientow(fraza):
    fraza = fraza.strip()
    if not fraza:
        return []
    warunek = Q(uzytkownik__last_name__icontains=fraza) | Q(uzytkownik__email__icontains=fraza) | Q(telefon__icontains=fraza)
    return [uzupelnij_saldo(p) for p in ProfilKlienta.objects.select_related('uzytkownik').filter(warunek)]


def karta_klienta(klient_id):
    from rezerwacje.services import rezerwacje_klienta
    profil = ProfilKlienta.objects.select_related('uzytkownik').filter(pk=klient_id).first()
    if not profil:
        return None
    lista = rezerwacje_klienta(profil.uzytkownik)
    aktualna = next((r for r in lista if r.dzien_odbioru == timezone.localdate() and r.stan in ('zlozona', 'przygotowana')), None)
    return SimpleNamespace(klient=uzupelnij_saldo(profil), rezerwacja_dzis=aktualna, rezerwacje=lista,
                           oplaty=_oplaty(lista), rozliczenia=RozliczenieZaleglosci.objects.filter(
                               klient=profil).select_related('zarejestrowal').order_by('-data_czas', '-pk'))


@transaction.atomic
def _odnotuj(klient_id, kwota, skuteczne, rodzaj, kto):
    profil = ProfilKlienta.objects.select_for_update().filter(pk=klient_id).first()
    if not profil or kwota <= 0 or kwota > uzupelnij_saldo(profil).zaleglosc:
        raise RozliczenieOdrzucone(_('Kwota musi być dodatnia i mieścić się w zaległości klienta.'))
    return RozliczenieZaleglosci.objects.create(klient=profil, kwota=kwota, skuteczne=skuteczne, rodzaj=rodzaj,
                                               data_czas=timezone.now(), zarejestrowal=kto)


def odnotuj_wplate(klient_id, kwota, kto):
    return _odnotuj(klient_id, kwota, True, 'wplata', kto)


def odnotuj_obciazenie(klient_id, kwota, skuteczne, kto):
    return _odnotuj(klient_id, kwota, skuteczne, 'obciazenie', kto)


def klienci_z_zaleglosci():
    profile = ProfilKlienta.objects.filter(rezerwacja__oplata_za_nieodebranie__gt=0).select_related('uzytkownik').distinct()
    dluznicy = (uzupelnij_saldo(p) for p in profile)
    return sorted((p for p in dluznicy if p.zaleglosc > 0), key=lambda p: -p.zaleglosc)


def _oplaty(lista):
    return [SimpleNamespace(rezerwacja_id=r.pk, dzien_odbioru=r.dzien_odbioru, wartosc=r.wartosc,
                            oplata_za_nieodebranie=r.oplata_za_nieodebranie)
            for r in lista if r.oplata_za_nieodebranie is not None]


def zaleglosc_klienta(uzytkownik):
    from rezerwacje.services import rezerwacje_klienta
    profil = uzupelnij_saldo(ProfilKlienta.objects.get(pk=uzytkownik.pk))
    profil.oplaty = _oplaty(rezerwacje_klienta(uzytkownik))
    return profil
