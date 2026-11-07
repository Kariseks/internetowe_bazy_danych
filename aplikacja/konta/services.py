"""Konta personelu i klientów. Na razie stuby, jak w magazyn/services.py."""
import atrapy


class KontoOdrzucone(Exception):
    """Np. zajęty login albo e-mail, ostatni aktywny właściciel. Panel wyświetla treść błędu."""


def lista_kont():
    """PU27. Obiekty User z dodatkowym polem rola (klient, sprzedawca, wlasciciel)."""
    return atrapy.konta()


def zaloz_sprzedawce(login, imie, nazwisko, email, haslo):
    """PU27, WF konta sprzedawców. Dokładnie jedna rola. Rzuca KontoOdrzucone."""
    raise NotImplementedError('zaloz_sprzedawce')


def ustaw_aktywnosc(konto_id, aktywne):
    """PU27. Sprzedawcę można dezaktywować i aktywować, klienta dezaktywować. Co najmniej jeden aktywny właściciel.

    Rzuca KontoOdrzucone.
    """
    raise NotImplementedError('ustaw_aktywnosc')


def zaloz_klienta(imie, nazwisko, email, telefon, haslo):
    """PU2 kroki 3–4. Konto z rolą klient, login = e-mail, bez karty. Zwraca User.

    Wysyła powiadomienia.konto_zalozone. Rzuca KontoOdrzucone, np. gdy e-mail jest zajęty.
    """
    raise NotImplementedError('zaloz_klienta')


def profil_klienta(uzytkownik):
    """PU7. Pola: uzytkownik, telefon, identyfikator_karty (None, gdy brak karty), zaleglosc, zablokowany."""
    return atrapy.profil_klienta(uzytkownik)


def zmien_telefon(uzytkownik, telefon):
    """PU7, WF dane konta: klient zmienia tylko numer telefonu."""
    raise NotImplementedError('zmien_telefon')


def zapisz_karte(uzytkownik_id, identyfikator_karty):
    """PU2 krok 7, PU13 krok 5. Nowy identyfikator w miejsce poprzedniego. Numer karty nie trafia do systemu."""
    raise NotImplementedError('zapisz_karte')
