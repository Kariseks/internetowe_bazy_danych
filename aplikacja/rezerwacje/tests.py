from datetime import timedelta
from decimal import Decimal
from unittest.mock import patch

from django.db import connection
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from magazyn.tests import konto

from . import services


class SzkieletTests(TestCase):
    def test_katalog_dostepny_bez_logowania(self):
        odpowiedz = self.client.get(reverse('katalog'))
        self.assertEqual(odpowiedz.status_code, 200)
        self.assertTemplateUsed(odpowiedz, 'rezerwacje/katalog.html')

    def test_panel_administratora_wymaga_logowania(self):
        odpowiedz = self.client.get('/admin/')
        self.assertRedirects(odpowiedz, '/admin/login/?next=/admin/')

    def test_baza_to_mysql(self):
        self.assertEqual(connection.vendor, 'mysql')


class PanelRezerwacjiTests(TestCase):
    def setUp(self):
        self.client.force_login(konto('sprzedawca', 'sprzedawca'))

    def test_polecenia_tylko_na_dzisiaj(self):
        self.assertContains(self.client.get('/admin/rezerwacje/'), '/rezerwacje/101/wydaj/')
        jutro = timezone.localdate() + timedelta(days=1)
        self.assertNotContains(self.client.get(f'/admin/rezerwacje/?dzien={jutro.isoformat()}'), '/wydaj/')

    def test_nieznana_rezerwacja(self):
        self.assertEqual(self.client.get('/admin/rezerwacje/999/wydaj/').status_code, 404)
        self.assertEqual(self.client.get('/admin/rezerwacje/999/przygotuj/').status_code, 404)

    def test_wydanie_zlozonej_zaczyna_od_wazenia(self):
        self.assertRedirects(
            self.client.get('/admin/rezerwacje/101/wydaj/'),
            '/admin/rezerwacje/101/przygotuj/?dalej=wydaj',
        )

    @patch('rezerwacje.services.przygotuj_rezerwacje')
    def test_przygotowanie_przyjmuje_zero_i_przechodzi_do_wydania(self, zapis):
        odpowiedz = self.client.post(
            '/admin/rezerwacje/101/przygotuj/?dalej=wydaj',
            {'p1': '9,95', 'p2': '0'},
        )
        self.assertEqual(zapis.call_args.args[1], [(1, Decimal('9.95')), (2, Decimal('0'))])
        self.assertEqual(odpowiedz.status_code, 302)
        self.assertEqual(odpowiedz.url, '/admin/rezerwacje/101/wydaj/')

    @patch('rezerwacje.services.wydaj_rezerwacje', side_effect=services.RezerwacjaOdrzucona('Po 18:00'))
    def test_wydanie_pokazuje_powod_odrzucenia(self, _):
        self.assertContains(self.client.post('/admin/rezerwacje/102/wydaj/', follow=True), 'Po 18:00')

    def pola_planu(self, **zmiany):
        pola = {}
        for wiersz in services.plan_tygodnia().wiersze:
            for k in wiersz.komorki:
                if not k.zamkniety:
                    pola[f'p{wiersz.produkt.id}-{k.dzien.isoformat()}'] = str(k.plan_kg)
        return {**pola, **zmiany}

    def test_sprzedawca_widzi_plan_bez_pol_i_nie_zapisze(self):
        self.assertNotContains(self.client.get('/admin/plan/'), 'Zapisz plan')
        self.assertEqual(self.client.post('/admin/plan/', self.pola_planu()).status_code, 403)

    @patch('rezerwacje.services.ustaw_plan', side_effect=services.PlanOdrzucony('Zarezerwowano 40 kg'))
    def test_wlasciciel_zmienia_tylko_zmienione_komorki(self, zapis):
        self.client.force_login(konto('wlasciciel', 'wlasciciel'))
        dzien = (timezone.localdate() + timedelta(days=3)).isoformat()
        odpowiedz = self.client.post(
            '/admin/plan/',
            self.pola_planu(**{f'p1-{dzien}': '5'}),
            follow=True,
        )
        zapis.assert_called_once()
        self.assertEqual(zapis.call_args.args[0], 1)
        self.assertEqual(zapis.call_args.args[2], Decimal('5'))
        self.assertContains(odpowiedz, 'Zarezerwowano 40 kg')
