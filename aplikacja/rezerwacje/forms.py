from django import forms
from django.core.exceptions import ValidationError
from django.utils.formats import localize

from magazyn.forms import pole_masy

from .services import LIMIT_KG


class RezerwacjaForm(forms.Form):
    """Pole ilości przy każdym produkcie oferty; puste albo 0 znaczy, że produktu nie rezerwuje się."""

    def __init__(self, oferta, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.oferta = oferta
        for wiersz in oferta:
            nazwa = f'p{wiersz.produkt.id}'
            self.fields[nazwa] = pole_masy(minimum='0', miejsca=1, required=False, label=str(wiersz.produkt))
            wiersz.pole = self[nazwa]

    def clean(self):
        dane = super().clean()
        if self.errors:
            return dane
        razem = 0
        for wiersz, ilosc in self.pozycje_z_wierszami():
            if ilosc > wiersz.dostepne_kg:
                self.add_error(f'p{wiersz.produkt.id}', f'Dostępne: {localize(wiersz.dostepne_kg)} kg.')
            razem += ilosc
        if not razem:
            raise ValidationError('Wpisz ilość co najmniej jednego produktu.')
        if razem > LIMIT_KG:
            raise ValidationError(f'Rezerwacja może mieć najwyżej {localize(LIMIT_KG)} kg, a ma {localize(razem)} kg.')
        return dane

    def pozycje_z_wierszami(self):
        return [(w, self.cleaned_data[f'p{w.produkt.id}']) for w in self.oferta if self.cleaned_data.get(f'p{w.produkt.id}')]

    def pozycje(self):
        """Lista (produkt_id, ilosc_kg) dla services."""
        return [(w.produkt.id, ilosc) for w, ilosc in self.pozycje_z_wierszami()]
