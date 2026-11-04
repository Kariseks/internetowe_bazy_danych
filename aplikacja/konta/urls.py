from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('logowanie/', views.Logowanie.as_view(), name='logowanie'),
    path('wyloguj/', views.Wylogowanie.as_view(), name='wyloguj'),
    path('haslo/reset/', views.ResetHasla.as_view(), name='haslo_reset'),
    # Ta nazwa włącza w logowaniu do panelu administratora odnośnik do resetu hasła.
    path('haslo/reset/', views.ResetHasla.as_view(), name='admin_password_reset'),
    path('haslo/nowe/<uidb64>/<token>/', views.NoweHaslo.as_view(), name='haslo_nowe'),
    path('haslo/zmienione/', views.HasloZmienione.as_view(), name='haslo_zmienione'),
    path('rejestracja/', TemplateView.as_view(template_name='konta/rejestracja.html'), name='rejestracja'),
]
