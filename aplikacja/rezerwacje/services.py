"""Reguły rezerwacji po stronie personelu. Na razie stuby, jak w magazyn/services.py.

Funkcje panelu klienta dojdą, gdy powstanie ten panel.
"""
import atrapy


class RezerwacjaOdrzucona(Exception):
    """Operacja niedozwolona w tym stanie albo po terminie. Panel wyświetla treść błędu."""


class PlanOdrzucony(Exception):
    """PU26 A1 i A2: plan poniżej zarezerwowanej ilości albo dzień zamknięty. Panel wyświetla treść błędu."""


def rezerwacje_na_dzien(dzien):
    """PU19. Pola: id, klient, dzien_odbioru, stan, zlozono, laczna_masa, pozycje.

    stan: zlozona, przygotowana, odebrana, anulowana, nieodebrana.
    klient: profil z polami uzytkownik, telefon, zaleglosc, zablokowany.
    Pozycja: produkt, ilosc_kg, masa_odwazona_kg.
    """
    return atrapy.rezerwacje(dzien)


def rezerwacja(rezerwacja_id):
    """Pola jak w rezerwacje_na_dzien. None, gdy nie istnieje."""
    return atrapy.rezerwacja(rezerwacja_id)


def przygotuj_rezerwacje(rezerwacja_id, masy, kto):
    """PU20 krok 4. masy: lista (produkt_id, masa_kg), także 0. Rzuca RezerwacjaOdrzucona."""
    raise NotImplementedError('przygotuj_rezerwacje')


def podsumowanie_wydania(rezerwacja_id):
    """PU21 krok 4. Pola: rezerwacja, do_zaplaty, pozycje. None, gdy nie istnieje.

    Pozycja: produkt, ilosc_kg, masa_kg, cena_za_kg (z dnia odbioru), wartosc.
    """
    return atrapy.wydanie(rezerwacja_id)


def wydaj_rezerwacje(rezerwacja_id, kto):
    """PU21 krok 6. Jedna transakcja: sprzedaż, stany, stan rezerwacji. Rzuca RezerwacjaOdrzucona."""
    raise NotImplementedError('wydaj_rezerwacje')


def plan_tygodnia():
    """PU26 krok 1. Pola: dni (dzien, zamkniety), wiersze (produkt, komorki).

    Komórka: dzien, zamkniety, plan_kg, zarezerwowano_kg, dostepne_kg, produkt.
    """
    return atrapy.plan_tygodnia()


def ustaw_plan(produkt_id, dzien, ilosc_kg):
    """PU26 krok 3. Blokuje wiersz planu. Rzuca PlanOdrzucony."""
    raise NotImplementedError('ustaw_plan')
