from decimal import Decimal

from .models import Produkt

from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone


def pole_masy(minimum='0.01', miejsca=2, **kwargs):
    return forms.DecimalField(
        min_value=Decimal(minimum),
        max_digits=7,
        decimal_places=miejsca,
        localize=True,
        widget=forms.TextInput(attrs={'inputmode': 'numeric' if miejsca == 0 else 'decimal', 'autocomplete': 'off'}),
        **kwargs,
    )


class IlosciForm(forms.Form):
    """Jedno pole masy na wiersz tabeli. Każdy wiersz dostaje swoje pole jako atrybut `pole`."""

    def __init__(self, wiersze, *args, klucz=lambda w: f'p{w.produkt.id}', poczatkowa=lambda w: None, **kwargs):
        super().__init__(*args, **kwargs)
        self.wiersze = [(wiersz, klucz(wiersz)) for wiersz in wiersze]
        for wiersz, nazwa in self.wiersze:
            sztuki = wiersz.produkt.jednostka == 'szt'
            poczatek = poczatkowa(wiersz)
            if sztuki and poczatek is not None:
                poczatek = int(poczatek)
            self.fields[nazwa] = pole_masy(minimum='0', miejsca=0 if sztuki else 2, initial=poczatek)
            wiersz.pole = self[nazwa]

    def wartosci(self):
        return [(wiersz, self.cleaned_data[nazwa]) for wiersz, nazwa in self.wiersze]


class PozycjaSprzedazyForm(forms.Form):
    produkt = forms.TypedChoiceField(coerce=int, widget=forms.HiddenInput)
    masa_kg = pole_masy()

    def __init__(self, *args, produkty=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['produkt'].choices = [(p.id, f'{p} [{p.symbol}]') for p in produkty]


class PozycjeSprzedazyFormSet(forms.BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        wybrane = [f.cleaned_data['produkt'] for f in self.forms if f.cleaned_data]
        if not wybrane:
            raise ValidationError(_('Wybierz co najmniej jeden produkt.'))
        if len(wybrane) != len(set(wybrane)):
            raise ValidationError(_('Ten sam produkt występuje na liście dwa razy.'))


SprzedazFormSet = forms.formset_factory(
    PozycjaSprzedazyForm,
    formset=PozycjeSprzedazyFormSet,
    extra=0,
)


def pole_ceny():
    return pole_masy(label=_('Cena jednostkowa [zł]'))


def pole_dnia_ceny():
    return forms.DateField(
        label=_('Obowiązuje od'),
        initial=timezone.localdate,
        widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
    )


class ProduktForm(forms.Form):
    nazwa = forms.CharField(label=_('Nazwa'), max_length=60)
    odmiana = forms.CharField(label=_('Odmiana'), max_length=60, required=False)
    standardowa_ilosc_kg = pole_masy(
        minimum='0',
        label=_('Standardowa dzienna ilość'),
        help_text=_('Ilość zamawiana zwykle na jeden dzień.'),
    )
    ilosc_na_lade_kg = pole_masy(minimum='0', label=_('Ilość na ladę'), initial=0)
    w_ofercie = forms.BooleanField(label=_('W ofercie'), required=False, initial=True)


class NowyProduktForm(ProduktForm):
    jednostka = forms.ChoiceField(label=_('Jednostka sprzedaży'), choices=[(kod, _(symbol)) for kod, symbol in Produkt.JEDNOSTKI], initial='kg', required=False)

    def clean_jednostka(self):
        return self.cleaned_data['jednostka'] or 'kg'

    cena_za_kg = pole_ceny()
    obowiazuje_od = pole_dnia_ceny()


class CenaForm(forms.Form):
    cena_za_kg = pole_ceny()
    obowiazuje_od = pole_dnia_ceny()


class KorektaForm(forms.Form):
    masa_kg = pole_masy(minimum='0', label=_('Ilość po przeliczeniu'))
    przyczyna = forms.CharField(label=_('Przyczyna korekty'), max_length=200)


class UbytekForm(forms.Form):
    produkt = forms.TypedChoiceField(label=_('Produkt'), coerce=int)
    masa_kg = pole_masy(label=_('Ilość wyrzuconego towaru'))

    def __init__(self, *args, produkty=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['produkt'].choices = [('', _('Wybierz produkt'))] + [(p.id, f'{p} [{p.symbol}]') for p in produkty]
