"""Reguły rezerwacji. Na razie stuby, jak w magazyn/services.py."""
from decimal import Decimal

import atrapy

LIMIT_KG = Decimal(20)


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


# Panel klienta. Rezerwacje klienta mają pola jak w rezerwacje_na_dzien oraz:
# termin (18:00 dnia poprzedniego), mozna_zmienic (złożona i przed terminem), wartosc (orientacyjna, ceny bieżące).


def katalog():
    """PU1. Produkty w ofercie. Pola jak w plan_tygodnia, wiersz ma też cena_za_kg (dzisiejsza)."""
    return atrapy.katalog()


def oferta_na_dzien(dzien, rezerwacja_id=None):
    """PU8 krok 2, PU9. Produkty w ofercie: produkt, cena_za_kg, dostepne_kg. Pusta lista, gdy dnia nie ma w katalogu.

    Przy zmianie rezerwacji (rezerwacja_id) dostepne_kg obejmuje też ilości tej rezerwacji.
    """
    return atrapy.oferta_na_dzien(dzien, rezerwacja_id)


def przeszkoda(uzytkownik, dzien):
    """PU8 krok 1. None, gdy klient może rezerwować na ten dzień. Inaczej pola: powod, rezerwacja, zaleglosc.

    powod: karta (brak karty), zaleglosc (ponad 100 zł, podać kwotę), istnieje (niezakończona rezerwacja
    na ten dzień, podać ją), zamkniete (dzień spoza katalogu albo po terminie).
    """
    return atrapy.przeszkoda(uzytkownik, dzien)


def rezerwacje_klienta(uzytkownik):
    """PU11. Wszystkie rezerwacje klienta, od najpóźniejszego dnia odbioru."""
    return atrapy.rezerwacje_klienta(uzytkownik)


def rezerwacja_klienta(uzytkownik, rezerwacja_id):
    """PU9, PU10. None, gdy nie istnieje albo należy do innego klienta."""
    return atrapy.rezerwacja_klienta(uzytkownik, rezerwacja_id)


def zloz_rezerwacje(uzytkownik, dzien, pozycje):
    """PU8 kroki 6–8. pozycje: lista (produkt_id, ilosc_kg) z ilością > 0.

    Jedna transakcja z blokadą planu dostawy (WF warunki złożenia); potem powiadomienia.rezerwacja(r, 'zlozona').
    Rzuca RezerwacjaOdrzucona z treścią do wyświetlenia (A3: podać aktualną ilość dostępną, A4, A5).
    """
    raise NotImplementedError('zloz_rezerwacje')


def zmien_rezerwacje(uzytkownik, rezerwacja_id, pozycje):
    """PU9. Jak zloz_rezerwacje, pozycje zastępują dotychczasowe; powiadomienie 'zmieniona'. Rzuca RezerwacjaOdrzucona."""
    raise NotImplementedError('zmien_rezerwacje')


def anuluj_rezerwacje(uzytkownik, rezerwacja_id):
    """PU10 kroki 3–5. Tylko złożona, przed terminem; zwalnia ilości w planie, powiadomienie 'anulowana'.

    Rzuca RezerwacjaOdrzucona.
    """
    raise NotImplementedError('anuluj_rezerwacje')
