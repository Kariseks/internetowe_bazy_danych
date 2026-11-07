from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from config.panel import obsluz_brak_logiki


def tylko_klient(widok):
    """Panel klienta: niezalogowany trafia na logowanie, personel dostaje 403 (pracuje w panelu administratora)."""
    @wraps(widok)
    def opakowany(request, *args, **kwargs):
        if request.user.is_staff:
            raise PermissionDenied
        return widok(request, *args, **kwargs)
    return login_required(opakowany)


def widok_klienta(widok):
    return tylko_klient(obsluz_brak_logiki(widok))
