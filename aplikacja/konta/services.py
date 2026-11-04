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
