from django.contrib.auth.forms import AuthenticationForm


class LogowanieForm(AuthenticationForm):
    error_messages = {
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
