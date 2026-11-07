"""Powiadomienia e-mail do klienta (WF powiadomienia, WF przypomnienie). Wywołują je services.

Rezerwacja ma pola jak w rezerwacje/services.py: klient (profil z uzytkownik, zaleglosc, zablokowany),
dzien_odbioru, termin, pozycje (produkt, ilosc_kg), oplata_za_nieodebranie.
"""
from django.core.mail import send_mail
from django.template.loader import render_to_string

TEMATY = {
    'zlozona': 'Warzywniak: rezerwacja złożona',
    'zmieniona': 'Warzywniak: rezerwacja zmieniona',
    'anulowana': 'Warzywniak: rezerwacja anulowana',
}


def _wyslij(temat, szablon, uzytkownik, **kontekst):
    tresc = render_to_string(f'powiadomienia/{szablon}.txt', {'uzytkownik': uzytkownik, **kontekst})
    send_mail(temat, tresc, None, [uzytkownik.email])


def konto_zalozone(uzytkownik):
    """PU2 krok 8."""
    _wyslij('Warzywniak: konto założone', 'konto', uzytkownik)


def rezerwacja(rezerwacja, zdarzenie):
    """PU8 krok 8, PU9, PU10 krok 5. zdarzenie: zlozona, zmieniona albo anulowana."""
    _wyslij(TEMATY[zdarzenie], 'rezerwacja', rezerwacja.klient.uzytkownik, rezerwacja=rezerwacja, zdarzenie=zdarzenie)


def oplata(rezerwacja):
    """PU30: opłata już naliczona, klient z zaległością po jej doliczeniu."""
    _wyslij('Warzywniak: opłata za nieodebraną rezerwację', 'oplata', rezerwacja.klient.uzytkownik, rezerwacja=rezerwacja)


def przypomnienie(rezerwacja, oplata):
    """PU31, o 6:00 w dniu odbioru. oplata: kwota, którą klient zapłaci, jeśli nie odbierze."""
    _wyslij('Warzywniak: odbiór rezerwacji dziś', 'przypomnienie', rezerwacja.klient.uzytkownik, rezerwacja=rezerwacja, oplata=oplata)
