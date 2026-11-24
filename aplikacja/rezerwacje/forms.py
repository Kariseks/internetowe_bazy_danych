from django import forms
from django.utils.translation import gettext_lazy as _
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
            self.fields[nazwa] = pole_masy(minimum='0', miejsca=0 if wiersz.produkt.jednostka == "szt" else 1, required=False, label=str(wiersz.produkt))
            wiersz.pole = self[nazwa]

    def clean(self):
        dane = super().clean()
        if self.errors:
            return dane
        razem = 0
        pozycje = self.pozycje_z_wierszami()
        for wiersz, ilosc in pozycje:
            if ilosc > wiersz.dostepne_kg:
                self.add_error(f'p{wiersz.produkt.id}', _('Dostępne: %(kg)s %(unit)s.') % {'kg': localize(wiersz.dostepne_kg), 'unit': wiersz.produkt.symbol})
            if wiersz.produkt.jednostka == "kg":
                razem += ilosc
        if not pozycje:
            raise ValidationError(_('Wpisz ilość co najmniej jednego produktu.'))
        if razem > LIMIT_KG:
            raise ValidationError(_('Rezerwacja może mieć najwyżej %(limit)s kg, a ma %(razem)s kg.') % {'limit': localize(LIMIT_KG), 'razem': localize(razem)})
        return dane

    def pozycje_z_wierszami(self):
        return [(w, self.cleaned_data[f'p{w.produkt.id}']) for w in self.oferta if self.cleaned_data.get(f'p{w.produkt.id}')]

    def pozycje(self):
        """Lista (produkt_id, ilosc_kg) dla services."""
        return [(w.produkt.id, ilosc) for w, ilosc in self.pozycje_z_wierszami()]
