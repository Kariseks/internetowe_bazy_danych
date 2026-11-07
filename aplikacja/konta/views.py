import secrets

from django.contrib import messages
from django.contrib.auth import views as auth
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from . import services
from .forms import LogowanieForm, RejestracjaForm, TelefonForm

# Konto założone w PU2, które czeka na rejestrację karty (klient nie jest jeszcze zalogowany).
NOWE_KONTO = 'nowe_konto'


class Logowanie(auth.LoginView):
    template_name = 'konta/logowanie.html'
    authentication_form = LogowanieForm
    redirect_authenticated_user = True
    next_page = 'katalog'


class Wylogowanie(auth.LogoutView):
    next_page = 'katalog'


class ResetHasla(SuccessMessageMixin, auth.PasswordResetView):
    template_name = 'konta/reset_hasla.html'
    email_template_name = 'konta/reset_email.txt'
    subject_template_name = 'konta/reset_temat.txt'
    success_url = reverse_lazy('haslo_reset')
    success_message = 'Jeśli to adres konta w sklepie, wysłaliśmy na niego link do ustawienia nowego hasła.'


class NoweHaslo(auth.PasswordResetConfirmView):
    template_name = 'konta/nowe_haslo.html'
    success_url = reverse_lazy('haslo_zmienione')


class HasloZmienione(auth.PasswordResetCompleteView):
    template_name = 'konta/haslo_zmienione.html'


class ZmianaHasla(SuccessMessageMixin, auth.PasswordChangeView):
    template_name = 'konta/zmiana_hasla.html'
    success_url = reverse_lazy('konto')
    success_message = 'Hasło zostało zmienione.'


def rejestracja(request):
    if request.user.is_authenticated:
        return redirect('katalog')
    form = RejestracjaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        dane = form.cleaned_data
        try:
            konto = services.zaloz_klienta(dane['imie'], dane['nazwisko'], dane['email'], dane['telefon'], dane['haslo'])
        except services.KontoOdrzucone as blad:
            form.add_error(None, str(blad))
        else:
            request.session[NOWE_KONTO] = konto.pk
            return redirect('karta')
    return render(request, 'konta/rejestracja.html', {'form': form})


def konto(request):
    profil = services.profil_klienta(request.user)
    form = TelefonForm(request.POST or None, initial={'telefon': profil.telefon})
    if request.method == 'POST' and form.is_valid():
        services.zmien_telefon(request.user, form.cleaned_data['telefon'])
        messages.success(request, 'Numer telefonu zmieniony.')
        return redirect('konto')
    return render(request, 'konta/konto.html', {'profil': profil, 'form': form})


def karta(request):
    """Symulowany formularz operatora płatności (wersja minimalna i standardowa, p. 2.5 sprawozdania).

    Służy klientowi (PU13) i kontu właśnie założonemu w PU2, zanim klient się zaloguje.
    """
    if request.user.is_authenticated and not request.user.is_staff:
        konto_id, nowe = request.user.pk, False
    elif not request.user.is_authenticated and NOWE_KONTO in request.session:
        konto_id, nowe = request.session[NOWE_KONTO], True
    else:
        return redirect('logowanie')
    if request.method == 'POST':
        if request.POST.get('wynik') == 'zatwierdz':
            # Operator zwraca identyfikator karty; numer karty nie trafia do systemu.
            services.zapisz_karte(konto_id, f'test_{secrets.token_hex(4)}')
            messages.success(request, 'Karta zarejestrowana.')
        else:
            messages.error(request, 'Nie zarejestrowano karty. Bez karty nie można składać rezerwacji.')
        if nowe:
            del request.session[NOWE_KONTO]
            messages.info(request, 'Konto założone. Zaloguj się adresem e-mail.')
            return redirect('logowanie')
        return redirect('konto')
    return render(request, 'konta/karta.html', {'nowe': nowe})
