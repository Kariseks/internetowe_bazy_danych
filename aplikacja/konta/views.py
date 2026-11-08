import secrets

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy

from . import operator, services
from .forms import LogowanieForm, RejestracjaForm, TelefonForm

# Konto założone w PU2, które czeka na rejestrację karty (klient nie jest jeszcze zalogowany).
NOWE_KONTO = 'nowe_konto'
# Sesja rejestracji karty u operatora, na którą czeka karta_powrot.
SESJA_OPERATORA = 'sesja_operatora'

BEZ_KARTY = 'Nie zarejestrowano karty. Bez karty nie można składać rezerwacji.'
OPERATOR_NIEDOSTEPNY = 'Operator płatności nie odpowiada. Karty nie zarejestrowano, spróbuj ponownie za chwilę.'


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


def _konto_do_karty(request):
    """(konto, nowe): zalogowany klient albo konto założone przed chwilą w PU2; (None, False), gdy żadne."""
    if request.user.is_authenticated and not request.user.is_staff:
        return request.user, False
    if not request.user.is_authenticated and NOWE_KONTO in request.session:
        return get_user_model().objects.filter(pk=request.session[NOWE_KONTO]).first(), True
    return None, False


def _po_karcie(request, nowe):
    if nowe:
        del request.session[NOWE_KONTO]
        messages.info(request, 'Konto założone. Zaloguj się adresem e-mail.')
        return redirect('logowanie')
    return redirect('konto')


def karta(request):
    """PU13 i PU2 krok 6: rejestracja karty u operatora płatności.

    Z kluczem Stripe przekierowuje na stronę operatora (wersja rozszerzona), bez klucza symuluje formularz
    operatora (wersja minimalna i standardowa, p. 2.5 sprawozdania). Służy klientowi i kontu właśnie
    założonemu w PU2, zanim klient się zaloguje.
    """
    konto, nowe = _konto_do_karty(request)
    if konto is None:
        return redirect('logowanie')
    if request.method == 'POST':
        if request.POST.get('wynik') != 'zatwierdz':
            messages.error(request, BEZ_KARTY)
            return _po_karcie(request, nowe)
        if operator.wlaczony():
            poprzednia = None if nowe else services.profil_klienta(konto).identyfikator_karty
            adres_powrotu = request.build_absolute_uri(reverse('karta_powrot'))
            try:
                sesja, adres = operator.rozpocznij(konto.pk, konto.email, poprzednia, adres_powrotu)
            except operator.OperatorNiedostepny:
                messages.error(request, OPERATOR_NIEDOSTEPNY)
                return redirect('karta')
            request.session[SESJA_OPERATORA] = sesja
            return redirect(adres)
        # Symulacja: operator zwraca identyfikator karty; numer karty nie trafia do systemu.
        services.zapisz_karte(konto.pk, f'test_{secrets.token_hex(4)}')
        messages.success(request, 'Karta zarejestrowana.')
        return _po_karcie(request, nowe)
    return render(request, 'konta/karta.html', {
        'nowe': nowe, 'operator': operator.wlaczony(), 'testowy': operator.testowy(),
    })


def karta_powrot(request):
    """Powrót ze strony operatora. Wynik sprawdza się u operatora; adres powrotu sam niczego nie potwierdza."""
    konto, nowe = _konto_do_karty(request)
    if konto is None:
        return redirect('logowanie')
    oczekiwana = request.session.pop(SESJA_OPERATORA, None)
    sesja = request.GET.get('sesja')
    if not sesja or sesja != oczekiwana:
        messages.error(request, BEZ_KARTY)
        return _po_karcie(request, nowe)
    try:
        karta_operatora = operator.zapisana_karta(sesja, konto.pk)
    except operator.OperatorNiedostepny:
        messages.error(request, OPERATOR_NIEDOSTEPNY)
        return redirect('karta')
    if karta_operatora is None:
        messages.error(request, BEZ_KARTY)
        return _po_karcie(request, nowe)
    poprzednia = None if nowe else services.profil_klienta(konto).identyfikator_karty
    services.zapisz_karte(konto.pk, karta_operatora)
    if poprzednia != karta_operatora:
        operator.odlacz(poprzednia)
    messages.success(request, 'Karta zarejestrowana.')
    return _po_karcie(request, nowe)
