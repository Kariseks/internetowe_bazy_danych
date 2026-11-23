from django.contrib import admin
from django.urls import include, path

from konta.dostep import widok_klienta
from rezerwacje.views import katalog
from rozliczenia.views import zaleglosc

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('', katalog, name='katalog'),
    path('', include('konta.urls')),
    path('', include('rezerwacje.urls')),
    path('zaleglosc/', widok_klienta(zaleglosc), name='zaleglosc'),
    path('admin/', admin.site.urls),
]
