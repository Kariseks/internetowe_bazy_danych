from django.urls import path

from config.panel import obsluz_brak_logiki

from . import views
from .dostep import tylko_klient, widok_klienta

urlpatterns = [
    path('logowanie/', views.Logowanie.as_view(), name='logowanie'),
    path('wyloguj/', views.Wylogowanie.as_view(), name='wyloguj'),
    path('haslo/reset/', views.ResetHasla.as_view(), name='haslo_reset'),
    # Ta nazwa włącza w logowaniu do panelu administratora odnośnik do resetu hasła.
    path('haslo/reset/', views.ResetHasla.as_view(), name='admin_password_reset'),
    path('haslo/nowe/<uidb64>/<token>/', views.NoweHaslo.as_view(), name='haslo_nowe'),
    path('haslo/zmienione/', views.HasloZmienione.as_view(), name='haslo_zmienione'),
    path('rejestracja/', obsluz_brak_logiki(views.rejestracja), name='rejestracja'),
    path('konto/', widok_klienta(views.konto), name='konto'),
    path('konto/haslo/', tylko_klient(views.ZmianaHasla.as_view()), name='zmiana_hasla'),
    path('konto/karta/', obsluz_brak_logiki(views.karta), name='karta'),
    # Powrót to GET: po błędzie stubu przekierowanie na ten sam adres zapętliłoby się.
    path('konto/karta/powrot/', obsluz_brak_logiki(views.karta_powrot, dokad='karta'), name='karta_powrot'),
]
