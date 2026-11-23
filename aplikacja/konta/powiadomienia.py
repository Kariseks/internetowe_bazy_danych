"""Powiadomienia e-mail do klienta (WF powiadomienia, WF przypomnienie). Wywołują je services.

Rezerwacja ma pola jak w rezerwacje/services.py: klient (profil z uzytkownik, zaleglosc, zablokowany),
dzien_odbioru, termin, pozycje (produkt, ilosc_kg), oplata_za_nieodebranie.
"""
from django.conf import settings
from django.utils.translation import gettext_lazy as _, override
from django.core.mail import send_mail
from django.template.loader import render_to_string

TEMATY = {
    'zlozona': _('Warzywniak: rezerwacja złożona'),
    'zmieniona': _('Warzywniak: rezerwacja zmieniona'),
    'anulowana': _('Warzywniak: rezerwacja anulowana'),
}


def _wyslij(temat, szablon, profil, **kontekst):
    uzytkownik = profil.uzytkownik
    with override(getattr(profil, 'jezyk', settings.LANGUAGE_CODE)):
        tresc = render_to_string(f'powiadomienia/{szablon}.txt', {'uzytkownik': uzytkownik, **kontekst})
        send_mail(str(temat), tresc, None, [uzytkownik.email])


def konto_zalozone(uzytkownik):
    """PU2 krok 8."""
    _wyslij(_('Warzywniak: konto założone'), 'konto', uzytkownik.profilklienta)


def rezerwacja(rezerwacja, zdarzenie):
    """PU8 krok 8, PU9, PU10 krok 5. zdarzenie: zlozona, zmieniona albo anulowana."""
    _wyslij(TEMATY[zdarzenie], 'rezerwacja', rezerwacja.klient, rezerwacja=rezerwacja, zdarzenie=zdarzenie)


def oplata(rezerwacja):
    """PU31: opłata już naliczona, klient z zaległością po jej doliczeniu."""
    _wyslij(_('Warzywniak: opłata za nieodebraną rezerwację'), 'oplata', rezerwacja.klient, rezerwacja=rezerwacja)


def przypomnienie(rezerwacja, oplata):
    """PU32, o 6:00 w dniu odbioru. oplata: kwota, którą klient zapłaci, jeśli nie odbierze."""
    _wyslij(_('Warzywniak: odbiór rezerwacji dziś'), 'przypomnienie', rezerwacja.klient, rezerwacja=rezerwacja, oplata=oplata)
