from datetime import timedelta
from functools import wraps

from django.contrib import admin, messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.utils.formats import date_format

from konta.role import jest_wlascicielem
from magazyn import services as magazyn
from rezerwacje import services as rezerwacje


def strona(request, szablon, tytul, **kontekst):
    return render(request, szablon, {**admin.site.each_context(request), 'title': tytul, **kontekst})


def tylko_wlasciciel(widok):
    @wraps(widok)
    def opakowany(request, *args, **kwargs):
        if not jest_wlascicielem(request.user):
            raise PermissionDenied
        return widok(request, *args, **kwargs)
    return opakowany


def obsluz_brak_logiki(widok):
    """Tymczasowe: zapis w stubie pokazuje komunikat zamiast błędu 500."""
    @wraps(widok)
    def opakowany(request, *args, **kwargs):
        try:
            return widok(request, *args, **kwargs)
        except NotImplementedError as blad:
            messages.warning(request, f'Formularz jest poprawny, ale nic nie zapisano: {blad} nie ma jeszcze logiki.')
            return redirect(request.get_full_path())
    return opakowany


def dzien_z_zapytania(request, domyslny=None, pole='dzien'):
    try:
        dzien = parse_date(request.GET.get(pole, ''))
    except ValueError:
        dzien = None
    if dzien and 2000 <= dzien.year <= 2100:
        return dzien
    return domyslny or timezone.localdate()


def nawigacja_dni(dzien):
    return {'dzien': dzien, 'dzien_wczesniej': dzien - timedelta(days=1), 'dzien_pozniej': dzien + timedelta(days=1)}


def pulpit(request):
    dzis = timezone.localdate()
    lista = rezerwacje.rezerwacje_na_dzien(dzis)
    return strona(
        request,
        'admin/panel/pulpit.html',
        date_format(dzis, 'l, j E'),
        dzis=dzis,
        dostawa=magazyn.dostawa_na_dzien(dzis),
        do_przygotowania=sum(r.stan == 'zlozona' for r in lista),
        do_odbioru=sum(r.stan in ('zlozona', 'przygotowana') for r in lista),
        lista=lista,
    )
