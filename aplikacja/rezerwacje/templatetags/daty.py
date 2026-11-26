"""Daty z dniem tygodnia w środku polskiego zdania.

Filtr ``date:"l"`` zwraca nazwę dnia w mianowniku wielką literą („Sobota”), co pasuje do nagłówka,
ale nie do zdania. Po angielsku obie funkcje zwracają to samo co ``date``.
"""
from django import template
from django.template.defaultfilters import date as formatuj
from django.utils.translation import get_language

register = template.Library()

BIERNIK = {
    'Poniedziałek': 'poniedziałek', 'Wtorek': 'wtorek', 'Środa': 'środę', 'Czwartek': 'czwartek',
    'Piątek': 'piątek', 'Sobota': 'sobotę', 'Niedziela': 'niedzielę',
}


def _zamien_dzien(tekst, odmiana):
    if not (get_language() or 'pl').startswith('pl'):
        return tekst
    for nazwa in BIERNIK:
        if tekst.startswith(nazwa):
            return odmiana(nazwa) + tekst[len(nazwa):]
    return tekst


@register.filter
def na_dzien(dzien, format='l, j E'):
    """Po przyimku „na”: „na sobotę, 28 listopada”."""
    return _zamien_dzien(formatuj(dzien, format), BIERNIK.get)


@register.filter
def w_zdaniu(dzien, format='l, j E'):
    """W środku zdania: „odbiór sobota, 28 listopada”."""
    return _zamien_dzien(formatuj(dzien, format), str.lower)
