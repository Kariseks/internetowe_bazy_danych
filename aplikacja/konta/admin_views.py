from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404, redirect
from .models import ProfilKlienta

from config.panel import strona

from . import services
from .role import jest_wlascicielem


class SprzedawcaForm(forms.Form):
    login = forms.CharField(label=_('Login'), max_length=150)
    imie = forms.CharField(label=_('Imię'), max_length=150)
    nazwisko = forms.CharField(label=_('Nazwisko'), max_length=150)
    email = forms.EmailField(label=_('Adres e-mail'))
    haslo = forms.CharField(label=_('Hasło'), widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))

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
                messages.success(request, _('Konto zaktualizowane.'))
            return redirect('admin:konta')
        form = SprzedawcaForm(request.POST)
        if form.is_valid():
            try:
                services.zaloz_sprzedawce(**form.cleaned_data)
            except services.KontoOdrzucone as blad:
                form.add_error(None, str(blad))
            else:
                messages.success(request, _('Konto sprzedawcy założone.'))
                return redirect('admin:konta')
    konta = services.lista_kont()
    return strona(
        request,
        'admin/panel/konta.html',
        _('Konta'),
        personel=[k for k in konta if k.rola != 'klient'],
        klienci=[k for k in konta if k.rola == 'klient'],
        form=form,
    )


class AnonimizacjaForm(forms.Form):
    potwierdz = forms.BooleanField(label=_('Potwierdzam trwałe usunięcie danych osobowych.'))


def anonimizacja(request, konto_id):
    profil = get_object_or_404(ProfilKlienta.objects.select_related('uzytkownik'), pk=konto_id)
    form = AnonimizacjaForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        try:
            services.anonimizuj_klienta(konto_id)
        except services.KontoOdrzucone as blad:
            form.add_error(None, str(blad))
        else:
            messages.success(request, _('Dane klienta zostały zanonimizowane.'))
            return redirect('admin:konta')
    return strona(request, 'admin/panel/anonimizacja.html', _('Anonimizacja klienta'), profil=profil, form=form)


def moje_konto(request):
    return strona(
        request,
        'admin/panel/moje_konto.html',
        _('Moje konto'),
        rola=_('właściciel') if jest_wlascicielem(request.user) else _('sprzedawca'),
    )
