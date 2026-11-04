from django import forms
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import redirect

from config.panel import strona

from . import services
from .role import jest_wlascicielem


class SprzedawcaForm(forms.Form):
    login = forms.CharField(label='Login', max_length=150)
    imie = forms.CharField(label='Imię', max_length=150)
    nazwisko = forms.CharField(label='Nazwisko', max_length=150)
    email = forms.EmailField(label='Adres e-mail')
    haslo = forms.CharField(label='Hasło', widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))

    def clean_haslo(self):
        validate_password(self.cleaned_data['haslo'])
        return self.cleaned_data['haslo']


def lista(request):
    form = SprzedawcaForm()
    if request.method == 'POST':
        konto_id = request.POST.get('konto', '')
        if konto_id.isdigit():
            try:
                services.ustaw_aktywnosc(int(konto_id), request.POST.get('aktywne') == '1')
            except services.KontoOdrzucone as blad:
                messages.error(request, str(blad))
            else:
                messages.success(request, 'Konto zaktualizowane.')
            return redirect('admin:konta')
        form = SprzedawcaForm(request.POST)
        if form.is_valid():
            try:
                services.zaloz_sprzedawce(**form.cleaned_data)
            except services.KontoOdrzucone as blad:
                form.add_error(None, str(blad))
            else:
                messages.success(request, 'Konto sprzedawcy założone.')
                return redirect('admin:konta')
    konta = services.lista_kont()
    return strona(
        request,
        'admin/panel/konta.html',
        'Konta',
        personel=[k for k in konta if k.rola != 'klient'],
        klienci=[k for k in konta if k.rola == 'klient'],
        form=form,
    )


def moje_konto(request):
    return strona(
        request,
        'admin/panel/moje_konto.html',
        'Moje konto',
        rola='właściciel' if jest_wlascicielem(request.user) else 'sprzedawca',
    )
