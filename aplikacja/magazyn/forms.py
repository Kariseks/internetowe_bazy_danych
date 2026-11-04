from decimal import Decimal

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone


def pole_masy(minimum='0.01', **kwargs):
    return forms.DecimalField(
        min_value=Decimal(minimum),
        max_digits=7,
        decimal_places=2,
        localize=True,
        widget=forms.TextInput(attrs={'inputmode': 'decimal', 'autocomplete': 'off'}),
        **kwargs,
    )


class IlosciForm(forms.Form):
    """Jedno pole masy na wiersz tabeli. Każdy wiersz dostaje swoje pole jako atrybut `pole`."""

    def __init__(self, wiersze, *args, klucz=lambda w: f'p{w.produkt.id}', poczatkowa=lambda w: None, **kwargs):
        super().__init__(*args, **kwargs)
        self.wiersze = [(wiersz, klucz(wiersz)) for wiersz in wiersze]
        for wiersz, nazwa in self.wiersze:
            self.fields[nazwa] = pole_masy(minimum='0', initial=poczatkowa(wiersz))
            wiersz.pole = self[nazwa]

    def wartosci(self):
        return [(wiersz, self.cleaned_data[nazwa]) for wiersz, nazwa in self.wiersze]


class PozycjaSprzedazyForm(forms.Form):
    produkt = forms.TypedChoiceField(coerce=int, widget=forms.HiddenInput)
    masa_kg = pole_masy()

    def __init__(self, *args, produkty=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['produkt'].choices = [(p.id, str(p)) for p in produkty]


class PozycjeSprzedazyFormSet(forms.BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        wybrane = [f.cleaned_data['produkt'] for f in self.forms if f.cleaned_data]
        if not wybrane:
            raise ValidationError('Wybierz co najmniej jeden produkt.')
        if len(wybrane) != len(set(wybrane)):
            raise ValidationError('Ten sam produkt występuje na liście dwa razy.')


SprzedazFormSet = forms.formset_factory(
    PozycjaSprzedazyForm,
    formset=PozycjeSprzedazyFormSet,
    extra=0,
)


def pole_ceny():
    return pole_masy(label='Cena za kg [zł]')


def pole_dnia_ceny():
    return forms.DateField(
        label='Obowiązuje od',
        initial=timezone.localdate,
        widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
    )


class ProduktForm(forms.Form):
    nazwa = forms.CharField(label='Nazwa', max_length=60)
    odmiana = forms.CharField(label='Odmiana', max_length=60, required=False)
    standardowa_ilosc_kg = pole_masy(
        minimum='0',
        label='Standardowa dzienna ilość [kg]',
        help_text='Ilość zamawiana zwykle na jeden dzień.',
    )
    w_ofercie = forms.BooleanField(label='W ofercie', required=False, initial=True)


class NowyProduktForm(ProduktForm):
    cena_za_kg = pole_ceny()
    obowiazuje_od = pole_dnia_ceny()


class CenaForm(forms.Form):
    cena_za_kg = pole_ceny()
    obowiazuje_od = pole_dnia_ceny()


class UbytekForm(forms.Form):
    produkt = forms.TypedChoiceField(label='Produkt', coerce=int)
    masa_kg = pole_masy(label='Masa wyrzuconego towaru [kg]')

    def __init__(self, *args, produkty=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['produkt'].choices = [('', 'Wybierz produkt')] + [(p.id, str(p)) for p in produkty]
