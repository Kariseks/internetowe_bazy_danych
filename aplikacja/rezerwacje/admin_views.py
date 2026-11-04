from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone

from config.panel import dzien_z_zapytania, nawigacja_dni, strona
from konta.role import jest_wlascicielem
from magazyn.forms import IlosciForm

from . import services


def lista(request):
    dzien = dzien_z_zapytania(request)
    return strona(
        request,
        'admin/panel/rezerwacje.html',
        'Rezerwacje',
        rezerwacje=services.rezerwacje_na_dzien(dzien),
        dzis=timezone.localdate(),
        **nawigacja_dni(dzien),
    )


def przygotuj(request, rezerwacja_id):
    rezerwacja = services.rezerwacja(rezerwacja_id)
    if rezerwacja is None:
        raise Http404
    do_wydania = request.GET.get('dalej') == 'wydaj'
    form = IlosciForm(rezerwacja.pozycje, request.POST or None, poczatkowa=lambda p: p.masa_odwazona_kg)
    if request.method == 'POST' and form.is_valid():
        masy = [(p.produkt.id, masa) for p, masa in form.wartosci()]
        try:
            services.przygotuj_rezerwacje(rezerwacja_id, masy, request.user)
        except services.RezerwacjaOdrzucona as blad:
            messages.error(request, str(blad))
        else:
            if do_wydania:
                return redirect('admin:wydaj', rezerwacja_id)
            messages.success(request, 'Rezerwacja jest przygotowana do odbioru.')
            return redirect('admin:rezerwacje')
    return strona(
        request,
        'admin/panel/przygotowanie.html',
        'Przygotowanie rezerwacji',
        rezerwacja=rezerwacja,
        form=form,
        do_wydania=do_wydania,
    )


def wydaj(request, rezerwacja_id):
    rezerwacja = services.rezerwacja(rezerwacja_id)
    if rezerwacja is None:
        raise Http404
    if rezerwacja.stan == 'zlozona':
        return redirect(reverse('admin:przygotuj', args=[rezerwacja_id]) + '?dalej=wydaj')
    if request.method == 'POST':
        try:
            services.wydaj_rezerwacje(rezerwacja_id, request.user)
        except services.RezerwacjaOdrzucona as blad:
            messages.error(request, str(blad))
        else:
            messages.success(request, 'Rezerwacja wydana.')
            return redirect('admin:rezerwacje')
    return strona(
        request,
        'admin/panel/wydanie.html',
        'Wydanie rezerwacji',
        wydanie=services.podsumowanie_wydania(rezerwacja_id),
    )


def plan(request):
    dane = services.plan_tygodnia()
    mozna_zmieniac = jest_wlascicielem(request.user)
    komorki = [k for wiersz in dane.wiersze for k in wiersz.komorki]
    form = IlosciForm(
        [k for k in komorki if not k.zamkniety],
        request.POST or None,
        klucz=lambda k: f'p{k.produkt.id}-{k.dzien.isoformat()}',
        poczatkowa=lambda k: k.plan_kg,
    )
    if request.method == 'POST':
        if not mozna_zmieniac:
            raise PermissionDenied
        if form.is_valid():
            zmiany = [(k, ilosc) for k, ilosc in form.wartosci() if ilosc != k.plan_kg]
            odrzucone = 0
            for komorka, ilosc in zmiany:
                try:
                    services.ustaw_plan(komorka.produkt.id, komorka.dzien, ilosc)
                except services.PlanOdrzucony as blad:
                    odrzucone += 1
                    messages.error(request, f'{komorka.produkt}, {komorka.dzien:%d.%m}: {blad}')
            if zmiany and not odrzucone:
                messages.success(request, 'Plan dostawy zapisany.')
            return redirect('admin:plan')
    return strona(request, 'admin/panel/plan.html', 'Plan dostawy', dane=dane, form=form, mozna_zmieniac=mozna_zmieniac)
