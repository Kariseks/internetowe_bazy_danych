"""Reguły magazynu. Na razie stuby: odczyty zwracają atrapy, zapisy rzucają NotImplementedError.

Panel korzysta z nazw pól podanych w opisach funkcji; model albo adnotacja o tej samej nazwie wystarczy.
"""
import atrapy


class ProduktOdrzucony(Exception):
    """Np. ta sama nazwa i odmiana albo druga cena od tego samego dnia. Panel wyświetla treść błędu."""


class BrakNaStanie(Exception):
    """Masa przekracza stan produktu. Treść błędu podaje produkt i bieżący stan; panel ją wyświetla."""


class DostawaOdrzucona(Exception):
    """Np. dostawa na ten dzień jest już zarejestrowana. Panel wyświetla treść błędu."""


def produkty():
    """PU24. Także wycofane: id, nazwa, odmiana, standardowa_ilosc_kg, w_ofercie, cena_za_kg (dzisiejsza)."""
    return atrapy.produkty_z_cenami()


def produkt(produkt_id):
    """PU24, PU25. Pola jak w produkty() oraz ceny (cena_za_kg, obowiazuje_od), najnowsze pierwsze. None, gdy brak."""
    return atrapy.produkt_z_historia_cen(produkt_id)


def dodaj_produkt(nazwa, odmiana, standardowa_ilosc_kg, w_ofercie, cena_za_kg, obowiazuje_od):
    """PU24. Produkt od razu z pierwszą ceną. Zwraca produkt (pole id). Rzuca ProduktOdrzucony."""
    raise NotImplementedError('dodaj_produkt')


def zmien_produkt(produkt_id, nazwa, odmiana, standardowa_ilosc_kg, w_ofercie):
    """PU24. Produktu się nie usuwa, tylko wycofuje z oferty (w_ofercie=False). Rzuca ProduktOdrzucony."""
    raise NotImplementedError('zmien_produkt')


def zmien_cene(produkt_id, cena_za_kg, obowiazuje_od):
    """PU25. Dopisuje cenę, wcześniejsze zostają. Rzuca ProduktOdrzucony."""
    raise NotImplementedError('zmien_cene')


def stan_produktow():
    """WF stan. Produkty w ofercie: produkt, cena_za_kg (dzisiejsza), stan_kg (dostawy − sprzedaż − ubytki)."""
    return atrapy.stan_produktow()


def plan_na_dzien(dzien):
    """PU14 krok 1, PU18. Produkty w ofercie: produkt, plan_kg, zarezerwowano_kg."""
    return atrapy.plan_na_dzien(dzien)


def dostawa_na_dzien(dzien):
    """PU14 krok 4. None, gdy brak dostawy. Pola: dzien, zarejestrowano, pozycje.

    Pozycja: produkt, plan_kg, zarezerwowano_kg, dostarczono_kg, roznica_kg, za_malo (dostarczono < zarezerwowano).
    """
    return atrapy.dostawa(dzien)


def zarejestruj_dostawe(dzien, pozycje, kto):
    """PU14 krok 3. pozycje: lista (produkt_id, ilosc_kg). Jedna transakcja. Rzuca DostawaOdrzucona."""
    raise NotImplementedError('zarejestruj_dostawe')


def zarejestruj_sprzedaz(pozycje, kto):
    """PU15 krok 6. pozycje: lista (produkt_id, masa_kg). Blokuje wiersze produktów, cena z chwili sprzedaży.

    Zwraca sprzedaż z polami id, suma. Rzuca BrakNaStanie, a wtedy niczego nie zapisuje.
    """
    raise NotImplementedError('zarejestruj_sprzedaz')


def zarejestruj_ubytek(produkt_id, masa_kg, kto):
    """WF ubytek. Blokuje wiersz produktu. Rzuca BrakNaStanie."""
    raise NotImplementedError('zarejestruj_ubytek')


def historia_sprzedazy(od, do):
    """WF stan. Najnowsze pierwsze: id, data_czas, sprzedawca, rezerwacja_id, suma, pozycje.

    Pozycja: produkt, masa_kg, cena_za_kg, wartosc.
    """
    return atrapy.historia_sprzedazy(od, do)


def zestawienia(od, do):
    """WF zestawienia (wersja rozszerzona). Pola:

    sprzedaz (produkt, masa_kg, wartosc), ubytki (produkt, masa_kg),
    roznice (produkt, plan_kg, dostarczono_kg, roznica_kg), nieodebrane (liczba, wartosc).
    """
    return atrapy.zestawienia(od, do)
