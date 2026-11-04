from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from magazyn.tests import konto

from . import services
from .role import jest_wlascicielem

STRONY_PERSONELU = [
    '/admin/',
    '/admin/sprzedaz/',
    '/admin/sprzedaz/historia/',
    '/admin/dostawa/',
    '/admin/ubytek/',
    '/admin/stan/',
    '/admin/zamowienie/',
    '/admin/rezerwacje/',
    '/admin/rezerwacje/101/przygotuj/',
    '/admin/rezerwacje/102/wydaj/',
    '/admin/plan/',
    '/admin/klienci/',
    '/admin/klienci/12/',
    '/admin/moje-konto/',
]
STRONY_WLASCICIELA = ['/admin/zaleglosci/', '/admin/konta/', '/admin/zestawienia/', '/admin/produkty/']


class RoleTests(TestCase):
    def test_jest_wlascicielem(self):
        self.assertTrue(jest_wlascicielem(konto('w', 'wlasciciel')))
        self.assertFalse(jest_wlascicielem(konto('s', 'sprzedawca')))


class DostepDoPaneluTests(TestCase):
    def test_sprzedawca(self):
        self.client.force_login(konto('s', 'sprzedawca'))
        for adres in STRONY_PERSONELU:
            self.assertEqual(self.client.get(adres).status_code, 200, adres)
        for adres in STRONY_WLASCICIELA:
            self.assertEqual(self.client.get(adres).status_code, 403, adres)

    def test_wlasciciel(self):
        self.client.force_login(konto('w', 'wlasciciel'))
        for adres in STRONY_PERSONELU + STRONY_WLASCICIELA:
            self.assertEqual(self.client.get(adres).status_code, 200, adres)

    def test_klient_i_niezalogowany_trafiaja_na_logowanie(self):
        klient = get_user_model().objects.create_user('k', password='x')
        for _ in ['niezalogowany', 'klient']:
            for adres in STRONY_PERSONELU + STRONY_WLASCICIELA:
                odpowiedz = self.client.get(adres)
                self.assertEqual(odpowiedz.status_code, 302, adres)
                self.assertIn('/admin/login/', odpowiedz.url)
            self.client.force_login(klient)

    def test_menu_ukrywa_strony_wlasciciela(self):
        self.client.force_login(konto('s', 'sprzedawca'))
        odpowiedz = self.client.get('/admin/')
        self.assertContains(odpowiedz, '/admin/sprzedaz/')
        self.assertNotContains(odpowiedz, '/admin/konta/')


class KontaTests(TestCase):
    def setUp(self):
        self.client.force_login(konto('w', 'wlasciciel'))

    def nowy(self, **pola):
        return {'login': 'anowak', 'imie': 'A', 'nazwisko': 'Nowak', 'email': 'a@example.com', 'haslo': 'Warzywa-2026!', **pola}

    @patch('konta.services.zaloz_sprzedawce')
    def test_nowy_sprzedawca(self, zapis):
        self.client.post('/admin/konta/', self.nowy())
        zapis.assert_called_once_with(login='anowak', imie='A', nazwisko='Nowak', email='a@example.com', haslo='Warzywa-2026!')

    @patch('konta.services.zaloz_sprzedawce')
    def test_slabe_haslo(self, zapis):
        self.client.post('/admin/konta/', self.nowy(haslo='12345678'))
        zapis.assert_not_called()

    @patch('konta.services.zaloz_sprzedawce', side_effect=services.KontoOdrzucone('Login zajęty'))
    def test_odrzucone_konto(self, _):
        self.assertContains(self.client.post('/admin/konta/', self.nowy()), 'Login zajęty')

    @patch('konta.services.ustaw_aktywnosc')
    def test_dezaktywacja(self, zapis):
        self.client.post('/admin/konta/', {'konto': '2', 'aktywne': '0'})
        zapis.assert_called_once_with(2, False)
