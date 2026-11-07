from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils.dateparse import parse_date

from . import services
from .forms import RezerwacjaForm

KONCOWE = ('odebrana', 'anulowana', 'nieodebrana')


def katalog(request):
    return render(request, 'rezerwacje/katalog.html', {'dane': services.katalog()})


def moje(request):
    rezerwacje = services.rezerwacje_klienta(request.user)
    return render(request, 'rezerwacje/moje.html', {
        'biezace': [r for r in rezerwacje if r.stan not in KONCOWE],
        'zakonczone': [r for r in rezerwacje if r.stan in KONCOWE],
    })


def nowa(request, dzien):
    try:
        dzien = parse_date(dzien)
    except ValueError:
        dzien = None
    if dzien is None:
        raise Http404
    przeszkoda = services.przeszkoda(request.user, dzien)
    if przeszkoda:
        return render(request, 'rezerwacje/przeszkoda.html', {'dzien': dzien, 'przeszkoda': przeszkoda})
    form = RezerwacjaForm(services.oferta_na_dzien(dzien), request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        try:
            services.zloz_rezerwacje(request.user, dzien, form.pozycje())
        except services.RezerwacjaOdrzucona as blad:
            form.add_error(None, str(blad))
        else:
            messages.success(request, 'Rezerwacja złożona. Potwierdzenie wysłaliśmy e-mailem.')
            return redirect('moje_rezerwacje')
    return render(request, 'rezerwacje/rezerwacja.html', {'dzien': dzien, 'form': form})


def rezerwacja_do_zmiany(request, rezerwacja_id):
    """Rezerwacja klienta, którą wolno jeszcze zmienić. None z komunikatem, gdy minął termin."""
    rezerwacja = services.rezerwacja_klienta(request.user, rezerwacja_id)
    if rezerwacja is None:
        raise Http404
    if rezerwacja.mozna_zmienic:
        return rezerwacja
    messages.error(request, 'Tej rezerwacji nie można już zmienić ani anulować. Nieodebranie jej spowoduje naliczenie opłaty.')
    return None


def zmien(request, rezerwacja_id):
    rezerwacja = rezerwacja_do_zmiany(request, rezerwacja_id)
    if rezerwacja is None:
        return redirect('moje_rezerwacje')
    oferta = services.oferta_na_dzien(rezerwacja.dzien_odbioru, rezerwacja_id)
    poczatkowe = {f'p{p.produkt.id}': p.ilosc_kg for p in rezerwacja.pozycje}
    form = RezerwacjaForm(oferta, request.POST if request.method == 'POST' else None, initial=poczatkowe)
    if request.method == 'POST' and form.is_valid():
        try:
            services.zmien_rezerwacje(request.user, rezerwacja_id, form.pozycje())
        except services.RezerwacjaOdrzucona as blad:
            form.add_error(None, str(blad))
        else:
            messages.success(request, 'Rezerwacja zmieniona. Potwierdzenie wysłaliśmy e-mailem.')
            return redirect('moje_rezerwacje')
    return render(request, 'rezerwacje/rezerwacja.html', {'dzien': rezerwacja.dzien_odbioru, 'form': form, 'rezerwacja': rezerwacja})


def anuluj(request, rezerwacja_id):
    rezerwacja = rezerwacja_do_zmiany(request, rezerwacja_id)
    if rezerwacja is None:
        return redirect('moje_rezerwacje')
    if request.method == 'POST':
        try:
            services.anuluj_rezerwacje(request.user, rezerwacja_id)
        except services.RezerwacjaOdrzucona as blad:
            messages.error(request, str(blad))
        else:
            messages.success(request, 'Rezerwacja anulowana bez opłaty.')
        return redirect('moje_rezerwacje')
    return render(request, 'rezerwacje/anulowanie.html', {'rezerwacja': rezerwacja})
