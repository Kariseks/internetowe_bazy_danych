from django.contrib import admin
from django.urls import include, path

from konta.dostep import widok_klienta
from rezerwacje.views import katalog
from rozliczenia.views import zaleglosc

urlpatterns = [
    path('', katalog, name='katalog'),
    path('', include('konta.urls')),
    path('', include('rezerwacje.urls')),
    path('zaleglosc/', widok_klienta(zaleglosc), name='zaleglosc'),
    path('admin/', admin.site.urls),
]
