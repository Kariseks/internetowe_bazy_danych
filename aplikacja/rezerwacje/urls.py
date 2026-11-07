from django.urls import path

from konta.dostep import widok_klienta

from . import views

urlpatterns = [
    path('rezerwacje/', widok_klienta(views.moje), name='moje_rezerwacje'),
    path('rezerwacje/nowa/<str:dzien>/', widok_klienta(views.nowa), name='nowa_rezerwacja'),
    path('rezerwacje/<int:rezerwacja_id>/zmien/', widok_klienta(views.zmien), name='zmien_rezerwacje'),
    path('rezerwacje/<int:rezerwacja_id>/anuluj/', widok_klienta(views.anuluj), name='anuluj_rezerwacje'),
]
