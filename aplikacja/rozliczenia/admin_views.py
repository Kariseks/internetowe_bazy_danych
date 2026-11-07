from django import forms
from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect

from config.panel import strona
from magazyn.forms import pole_masy

from . import services


class KwotaForm(forms.Form):
    kwota = pole_masy(label='Kwota [zł]')


def klienci(request):
    fraza = request.GET.get('q', '')
    return strona(
        request,
        'admin/panel/klienci.html',
        'Klienci',
        fraza=fraza,
        wyniki=services.wyszukaj_klientow(fraza),
    )


def karta(request, klient_id):
    dane = services.karta_klienta(klient_id)
    if dane is None:
        raise Http404
    form = KwotaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        try:
            services.odnotuj_wplate(klient_id, form.cleaned_data['kwota'], request.user)
        except services.RozliczenieOdrzucone as blad:
            form.add_error('kwota', str(blad))
        else:
            messages.success(request, 'Wpłata odnotowana.')
            return redirect('admin:karta_klienta', klient_id)
    return strona(request, 'admin/panel/karta_klienta.html', dane.klient.uzytkownik.get_full_name(), dane=dane, form=form)


def zaleglosci(request):
    if request.method == 'POST':
        form = KwotaForm(request.POST)
        klient_id = request.POST.get('klient', '')
        if form.is_valid() and klient_id.isdigit():
            try:
                services.odnotuj_obciazenie(
                    int(klient_id),
                    form.cleaned_data['kwota'],
                    request.POST.get('wynik') == 'skuteczne',
                    request.user,
                )
            except services.RozliczenieOdrzucone as blad:
                messages.error(request, str(blad))
            else:
                messages.success(request, 'Wynik obciążenia odnotowany.')
        else:
            messages.error(request, 'Podaj poprawną kwotę, np. 12,40.')
        return redirect('admin:zaleglosci')
    return strona(request, 'admin/panel/zaleglosci.html', 'Zaległości klientów', klienci=services.klienci_z_zaleglosci())
