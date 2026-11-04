from django.contrib import admin
from django.urls import path

from konta import admin_views as konta
from konta.role import jest_wlascicielem
from magazyn import admin_views as magazyn
from rezerwacje import admin_views as rezerwacje
from rozliczenia import admin_views as rozliczenia

from .panel import obsluz_brak_logiki, pulpit, tylko_wlasciciel


class SklepAdminSite(admin.AdminSite):
    site_header = 'Warzywniak'
    site_title = 'Warzywniak'
    enable_nav_sidebar = False

    def each_context(self, request):
        kontekst = super().each_context(request)
        kontekst['jest_wlascicielem'] = request.user.is_authenticated and jest_wlascicielem(request.user)
        return kontekst

    def index(self, request, extra_context=None):
        return pulpit(request)

    def get_urls(self):
        def strona(trasa, widok, nazwa):
            return path(trasa, self.admin_view(obsluz_brak_logiki(widok)), name=nazwa)

        return [
            strona('sprzedaz/', magazyn.sprzedaz, 'sprzedaz'),
            strona('sprzedaz/historia/', magazyn.historia, 'historia'),
            strona('dostawa/', magazyn.dostawa, 'dostawa'),
            strona('ubytek/', magazyn.ubytek, 'ubytek'),
            strona('stan/', magazyn.stan, 'stan'),
            strona('zamowienie/', magazyn.zamowienie, 'zamowienie'),
            strona('zestawienia/', tylko_wlasciciel(magazyn.zestawienia), 'zestawienia'),
            strona('produkty/', tylko_wlasciciel(magazyn.produkty), 'produkty'),
            strona('produkty/nowy/', tylko_wlasciciel(magazyn.produkt_nowy), 'produkt_nowy'),
            strona('produkty/<int:produkt_id>/', tylko_wlasciciel(magazyn.produkt_edycja), 'produkt_edycja'),
            strona('rezerwacje/', rezerwacje.lista, 'rezerwacje'),
            strona('rezerwacje/<int:rezerwacja_id>/przygotuj/', rezerwacje.przygotuj, 'przygotuj'),
            strona('rezerwacje/<int:rezerwacja_id>/wydaj/', rezerwacje.wydaj, 'wydaj'),
            strona('plan/', rezerwacje.plan, 'plan'),
            strona('klienci/', rozliczenia.klienci, 'klienci'),
            strona('klienci/<int:klient_id>/', rozliczenia.karta, 'karta_klienta'),
            strona('zaleglosci/', tylko_wlasciciel(rozliczenia.zaleglosci), 'zaleglosci'),
            strona('konta/', tylko_wlasciciel(konta.lista), 'konta'),
            strona('moje-konto/', konta.moje_konto, 'moje_konto'),
            *super().get_urls(),
        ]
