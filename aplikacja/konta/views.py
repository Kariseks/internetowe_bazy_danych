from django.contrib.auth import views as auth
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from .forms import LogowanieForm


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
