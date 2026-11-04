from datetime import timedelta

from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from django.utils import timezone

from config.panel import dzien_z_zapytania, nawigacja_dni, strona

from . import services
from .forms import (
    CenaForm,
    IlosciForm,
    NowyProduktForm,
    ProduktForm,
    SprzedazFormSet,
    UbytekForm,
)


def sprzedaz(request):
    wiersze = services.stan_produktow()
    produkty = [w.produkt for w in wiersze]
    formset = SprzedazFormSet(request.POST or None, form_kwargs={'produkty': produkty})
    if request.method == 'POST' and formset.is_valid():
        pozycje = [(f.cleaned_data['produkt'], f.cleaned_data['masa_kg']) for f in formset if f.cleaned_data]
        try:
            zapisana = services.zarejestruj_sprzedaz(pozycje, request.user)
        except services.BrakNaStanie as blad:
            messages.error(request, str(blad))
        else:
            messages.success(request, f'Sprzedaż zapisana. Do zapłaty: {zapisana.suma} zł.')
            return redirect('admin:sprzedaz')
    return strona(request, 'admin/panel/sprzedaz.html', 'Nowa sprzedaż', wiersze=wiersze, formset=formset)


def historia(request):
    dzien = dzien_z_zapytania(request)
    return strona(
        request,
        'admin/panel/historia.html',
        'Historia sprzedaży',
        sprzedaze=services.historia_sprzedazy(dzien, dzien),
        **nawigacja_dni(dzien),
    )


def dostawa(request):
    dzis = timezone.localdate()
    dzien = dzien_z_zapytania(request)
    przyjeta = services.dostawa_na_dzien(dzien)
    kontekst = {'przyjeta': przyjeta, 'dzis': dzis, **nawigacja_dni(dzien)}
    if przyjeta is None and dzien == dzis:
        wiersze = services.plan_na_dzien(dzis)
        form = IlosciForm(wiersze, request.POST or None)
        if request.method == 'POST' and form.is_valid():
            pozycje = [(w.produkt.id, ilosc) for w, ilosc in form.wartosci()]
            try:
                services.zarejestruj_dostawe(dzis, pozycje, request.user)
            except services.DostawaOdrzucona as blad:
                messages.error(request, str(blad))
            else:
                messages.success(request, 'Dostawa zapisana.')
                return redirect('admin:dostawa')
        kontekst.update(form=form, wiersze=wiersze)
    return strona(request, 'admin/panel/dostawa.html', 'Przyjęcie dostawy', **kontekst)


def ubytek(request):
    produkty = [w.produkt for w in services.stan_produktow()]
    form = UbytekForm(request.POST or None, produkty=produkty)
    if request.method == 'POST' and form.is_valid():
        try:
            services.zarejestruj_ubytek(form.cleaned_data['produkt'], form.cleaned_data['masa_kg'], request.user)
        except services.BrakNaStanie as blad:
            form.add_error('masa_kg', str(blad))
        else:
            messages.success(request, 'Ubytek zapisany.')
            return redirect('admin:ubytek')
    return strona(request, 'admin/panel/ubytek.html', 'Ubytek towaru', form=form)


def stan(request):
    return strona(request, 'admin/panel/stan.html', 'Stan produktów', wiersze=services.stan_produktow())


def zamowienie(request):
    jutro = timezone.localdate() + timedelta(days=1)
    wiersze = services.plan_na_dzien(jutro)
    return strona(
        request,
        'admin/panel/zamowienie.html',
        'Zamówienie u dostawcy',
        jutro=jutro,
        wiersze=wiersze,
        razem=sum(w.plan_kg for w in wiersze),
    )


def zestawienia(request):
    dzis = timezone.localdate()
    od = dzien_z_zapytania(request, dzis - timedelta(days=30), pole='od')
    do = dzien_z_zapytania(request, dzis, pole='do')
    return strona(
        request,
        'admin/panel/zestawienia.html',
        'Zestawienia',
        od=od,
        do=do,
        dane=services.zestawienia(od, do),
    )


def produkty(request):
    return strona(request, 'admin/panel/produkty.html', 'Produkty i ceny', produkty=services.produkty())


def produkt_nowy(request):
    form = NowyProduktForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        try:
            services.dodaj_produkt(**form.cleaned_data)
        except services.ProduktOdrzucony as blad:
            form.add_error(None, str(blad))
        else:
            messages.success(request, 'Produkt dodany.')
            return redirect('admin:produkty')
    return strona(request, 'admin/panel/produkt_nowy.html', 'Nowy produkt', form=form)


def produkt_edycja(request, produkt_id):
    produkt = services.produkt(produkt_id)
    if produkt is None:
        raise Http404
    zmiana_ceny = 'zapisz_cene' in request.POST
    form = ProduktForm(
        request.POST if request.method == 'POST' and not zmiana_ceny else None,
        initial={
            'nazwa': produkt.nazwa,
            'odmiana': produkt.odmiana,
            'standardowa_ilosc_kg': produkt.standardowa_ilosc_kg,
            'w_ofercie': produkt.w_ofercie,
        },
    )
    form_ceny = CenaForm(request.POST if zmiana_ceny else None)
    if request.method == 'POST':
        aktywny, zapis, komunikat = (
            (form_ceny, services.zmien_cene, 'Cena zapisana.')
            if zmiana_ceny
            else (form, services.zmien_produkt, 'Produkt zapisany.')
        )
        if aktywny.is_valid():
            try:
                zapis(produkt_id, **aktywny.cleaned_data)
            except services.ProduktOdrzucony as blad:
                aktywny.add_error(None, str(blad))
            else:
                messages.success(request, komunikat)
                return redirect('admin:produkt_edycja', produkt_id)
    return strona(request, 'admin/panel/produkt.html', str(produkt), produkt=produkt, form=form, form_ceny=form_ceny)
