"""Konta Django i dane klientów sklepu."""
from uuid import uuid4

from django.contrib.auth.models import Group, User
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext as _

from . import powiadomienia
from .models import ProfilKlienta
from .role import jest_wlascicielem


class KontoOdrzucone(Exception):
    pass


def lista_kont():
    konta = list(User.objects.prefetch_related('groups').order_by('last_name', 'username'))
    for konto in konta:
        grupy = {g.name for g in konto.groups.all()}
        konto.rola = 'wlasciciel' if konto.is_superuser or 'wlasciciel' in grupy else (
            'sprzedawca' if konto.is_staff else 'klient')
    return konta


def _utworz(login, imie, nazwisko, email, haslo, rola):
    if User.objects.filter(Q(username__iexact=login) | Q(email__iexact=email)).exists():
        raise KontoOdrzucone(_('Ten login lub adres e-mail jest już zajęty.'))
    try:
        with transaction.atomic():
            user = User.objects.create_user(login, email, haslo, first_name=imie, last_name=nazwisko,
                                            is_staff=rola == 'sprzedawca')
            grupa, _nowa = Group.objects.get_or_create(name=rola)
            user.groups.add(grupa)
    except IntegrityError as blad:
        raise KontoOdrzucone(_('Ten login lub adres e-mail jest już zajęty.')) from blad
    return user


def zaloz_sprzedawce(login, imie, nazwisko, email, haslo):
    return _utworz(login, imie, nazwisko, email.lower(), haslo, 'sprzedawca')


@transaction.atomic
def ustaw_aktywnosc(konto_id, aktywne):
    # Obie próby równoczesnej dezaktywacji muszą zobaczyć tę samą listę właścicieli.
    personel = list(User.objects.select_for_update().filter(is_staff=True).order_by('pk'))
    konto = User.objects.select_for_update().filter(pk=konto_id).first()
    if not konto:
        raise KontoOdrzucone(_('Nie znaleziono konta.'))
    if aktywne and not konto.is_staff:
        raise KontoOdrzucone(_('Aktywować można tylko konto personelu.'))
    if not aktywne and konto.is_active and jest_wlascicielem(konto) and not any(
        p.pk != konto.pk and p.is_active and jest_wlascicielem(p) for p in personel
    ):
        raise KontoOdrzucone(_('Sklep musi mieć co najmniej jednego aktywnego właściciela.'))
    konto.is_active = aktywne
    konto.save(update_fields=['is_active'])


def zaloz_klienta(imie, nazwisko, email, telefon, haslo):
    email = email.strip().lower()
    with transaction.atomic():
        user = _utworz(email, imie, nazwisko, email, haslo, 'klient')
        ProfilKlienta.objects.create(uzytkownik=user, telefon=telefon, regulamin_zaakceptowano=timezone.now())
    powiadomienia.konto_zalozone(user)
    return user


def profil_klienta(uzytkownik):
    from rozliczenia.services import uzupelnij_saldo
    return uzupelnij_saldo(ProfilKlienta.objects.select_related('uzytkownik').get(pk=uzytkownik.pk))


def zmien_telefon(uzytkownik, telefon):
    ProfilKlienta.objects.filter(pk=uzytkownik.pk, zanonimizowano__isnull=True).update(telefon=telefon)


def zapisz_karte(uzytkownik_id, identyfikator_karty):
    ProfilKlienta.objects.filter(pk=uzytkownik_id, zanonimizowano__isnull=True).update(identyfikator_karty=identyfikator_karty)


@transaction.atomic
def anonimizuj_klienta(konto_id):
    from rezerwacje.models import Rezerwacja
    from rozliczenia.services import uzupelnij_saldo
    profil = ProfilKlienta.objects.select_for_update().filter(pk=konto_id).first()
    if not profil:
        raise KontoOdrzucone(_('Nie znaleziono konta.'))
    if profil.zanonimizowano:
        return
    if uzupelnij_saldo(profil).zaleglosc or Rezerwacja.objects.filter(
            klient=profil, stan__in=('zlozona', 'przygotowana')).exists():
        raise KontoOdrzucone(_('Najpierw zakończ rezerwacje i rozlicz zaległość.'))
    user = profil.uzytkownik
    user.username = 'anon-' + uuid4().hex
    user.first_name = user.last_name = user.email = ''
    user.is_active = False
    user.set_unusable_password()
    user.save()
    profil.telefon = ''
    profil.zanonimizowano = timezone.now()
    profil.identyfikator_karty = None
    profil.save()
