"""Zaległości i rozliczenia. Na razie stuby, jak w magazyn/services.py."""
import atrapy


class RozliczenieOdrzucone(Exception):
    """Wpłata albo obciążenie niedozwolone. Panel wyświetla treść błędu."""


def wyszukaj_klientow(fraza):
    """PU22. Po nazwisku, e-mailu albo telefonie. Pusta fraza: pusta lista.

    Profil: uzytkownik_id, uzytkownik, telefon, identyfikator_karty, zaleglosc, zablokowany.
    """
    fraza = fraza.strip().lower()
    if not fraza:
        return []
    return [
        k for k in atrapy.klienci()
        if fraza in k.uzytkownik.last_name.lower() or fraza in k.uzytkownik.email or fraza in k.telefon
    ]


def karta_klienta(klient_id):
    """PU22. None, gdy nie istnieje. Pola: klient, rezerwacja_dzis, rezerwacje, oplaty, rozliczenia.

    Opłata: rezerwacja_id, dzien_odbioru, oplata_za_nieodebranie.
    Rozliczenie: data_czas, rodzaj (wplata, obciazenie), kwota, skuteczne, zarejestrowal.
    """
    return atrapy.karta_klienta(klient_id)


def odnotuj_wplate(klient_id, kwota, kto):
    """PU23. Rzuca RozliczenieOdrzucone."""
    raise NotImplementedError('odnotuj_wplate')


def klienci_z_zaleglosci():
    """PU28. Profile z zaleglosc > 0, od największej."""
    return sorted((k for k in atrapy.klienci() if k.zaleglosc), key=lambda k: -k.zaleglosc)


def odnotuj_obciazenie(klient_id, kwota, skuteczne, kto):
    """PU28. Skuteczne zmniejsza zaległość o kwotę, nieudane jej nie zmienia. Rzuca RozliczenieOdrzucone."""
    raise NotImplementedError('odnotuj_obciazenie')


def zaleglosc_klienta(uzytkownik):
    """PU12. Pola: zaleglosc, zablokowany, oplaty (rezerwacja_id, dzien_odbioru, wartosc, oplata_za_nieodebranie)."""
    return atrapy.zaleglosc_klienta(uzytkownik)
