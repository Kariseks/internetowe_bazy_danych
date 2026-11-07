from typing import ClassVar

from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class LogowanieForm(AuthenticationForm):
    error_messages: ClassVar[dict] = {
        **AuthenticationForm.error_messages,
        'invalid_login': 'Niepoprawny login lub hasło.',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Login'

    def confirm_login_allowed(self, user):
        # Personel loguje się w panelu administratora, dostępnym tylko z sieci sklepu.
        super().confirm_login_allowed(user)
        if user.is_staff:
            raise self.get_invalid_login_error()


def pole_telefonu():
    return forms.CharField(
        label='Numer telefonu',
        max_length=20,
        validators=[RegexValidator(r'^\+?[\d -]{9,19}$', 'Podaj numer telefonu, np. 501 200 300.')],
        widget=forms.TextInput(attrs={'autocomplete': 'tel', 'inputmode': 'tel'}),
    )


class RejestracjaForm(forms.Form):
    imie = forms.CharField(label='Imię', max_length=150, widget=forms.TextInput(attrs={'autocomplete': 'given-name'}))
    nazwisko = forms.CharField(label='Nazwisko', max_length=150, widget=forms.TextInput(attrs={'autocomplete': 'family-name'}))
    email = forms.EmailField(label='Adres e-mail', help_text='Adres e-mail jest loginem do konta.')
    telefon = pole_telefonu()
    haslo = forms.CharField(
        label='Hasło',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    haslo2 = forms.CharField(label='Powtórz hasło', widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(username__iexact=email).exists():
            raise ValidationError('Konto z tym adresem e-mail już istnieje.')
        return email

    def clean(self):
        dane = super().clean()
        haslo = dane.get('haslo')
        if haslo and haslo != dane.get('haslo2'):
            self.add_error('haslo2', 'Hasła nie są takie same.')
        elif haslo:
            kandydat = User(username=dane.get('email', ''), email=dane.get('email', ''),
                            first_name=dane.get('imie', ''), last_name=dane.get('nazwisko', ''))
            try:
                password_validation.validate_password(haslo, kandydat)
            except ValidationError as blad:
                self.add_error('haslo', blad)
        return dane


class TelefonForm(forms.Form):
    telefon = pole_telefonu()
