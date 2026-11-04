from decimal import Decimal
from unittest.mock import patch

from django.test import TestCase

from magazyn.tests import konto

from . import services


class PanelRozliczenTests(TestCase):
    def setUp(self):
        self.client.force_login(konto('sprzedawca', 'sprzedawca'))

    def test_wyszukiwanie(self):
        self.assertContains(self.client.get('/admin/klienci/?q=kowal'), 'Anna Kowalska')
        self.assertContains(self.client.get('/admin/klienci/?q=nikt'), 'Nikt nie pasuje')
        self.assertNotContains(self.client.get('/admin/klienci/'), 'Anna Kowalska')

    def test_nieznany_klient(self):
        self.assertEqual(self.client.get('/admin/klienci/999/').status_code, 404)

    @patch('rozliczenia.services.odnotuj_wplate')
    def test_wplata(self, zapis):
        self.client.post('/admin/klienci/12/', {'kwota': '0'})
        zapis.assert_not_called()
        self.client.post('/admin/klienci/12/', {'kwota': '12,40'})
        self.assertEqual(zapis.call_args.args[:2], (12, Decimal('12.40')))

    @patch('rozliczenia.services.odnotuj_wplate', side_effect=services.RozliczenieOdrzucone('Za dużo'))
    def test_wplata_odrzucona(self, _):
        self.assertContains(self.client.post('/admin/klienci/12/', {'kwota': '999'}), 'Za dużo')

    def test_zaleglosci_tylko_dla_wlasciciela(self):
        self.assertEqual(self.client.get('/admin/zaleglosci/').status_code, 403)

    def test_enter_nie_wybiera_wyniku_obciazenia(self):
        self.client.force_login(konto('wlasciciel', 'wlasciciel'))
        strona = self.client.get('/admin/zaleglosci/').content.decode()
        formularz = strona[strona.index('<form method="post" class="w-wierszu">'):]
        self.assertLess(formularz.index('type="submit" disabled'), formularz.index('value="skuteczne"'))

    @patch('rozliczenia.services.odnotuj_obciazenie')
    def test_wynik_obciazenia(self, zapis):
        self.client.force_login(konto('wlasciciel', 'wlasciciel'))
        self.client.post('/admin/zaleglosci/', {'klient': '14', 'kwota': '118,60', 'wynik': 'skuteczne'})
        self.assertEqual(zapis.call_args.args[:3], (14, Decimal('118.60'), True))
        self.client.post('/admin/zaleglosci/', {'klient': '14', 'kwota': '118,60', 'wynik': 'nieudane'})
        self.assertEqual(zapis.call_args.args[:3], (14, Decimal('118.60'), False))
        zapis.reset_mock()
        odpowiedz = self.client.post('/admin/zaleglosci/', {'klient': '14', 'kwota': 'abc'}, follow=True)
        zapis.assert_not_called()
        self.assertContains(odpowiedz, 'Podaj poprawną kwotę')
