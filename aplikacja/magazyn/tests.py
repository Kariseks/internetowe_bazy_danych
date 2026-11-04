from datetime import timedelta
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.utils import timezone

from . import services
from .services import BrakNaStanie


def konto(login, *grupy, **pola):
    user = get_user_model().objects.create_user(login, password='x', is_staff=True, **pola)
    for nazwa in grupy:
        user.groups.add(Group.objects.get_or_create(name=nazwa)[0])
    return user


class PanelMagazynuTests(TestCase):
    def setUp(self):
        self.client.force_login(konto('sprzedawca', 'sprzedawca'))

    def test_nowa_sprzedaz_nie_ma_pustego_wiersza(self):
        self.assertEqual(self.client.get('/admin/sprzedaz/').context['formset'].total_form_count(), 0)

    def sprzedaj(self, *pozycje):
        dane = {
            'form-TOTAL_FORMS': str(len(pozycje)),
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',
        }
        for i, (produkt, masa) in enumerate(pozycje):
            dane[f'form-{i}-produkt'] = produkt
            dane[f'form-{i}-masa_kg'] = masa
        return self.client.post('/admin/sprzedaz/', dane, follow=True)

    @patch('magazyn.services.zarejestruj_sprzedaz')
    def test_sprzedaz_przekazuje_pozycje_z_przecinkiem(self, zapis):
        zapis.return_value = SimpleNamespace(suma=Decimal('8.00'))
        odpowiedz = self.sprzedaj(('1', '2,50'), ('4', '1,2'))
        zapis.assert_called_once()
        self.assertEqual(zapis.call_args.args[0], [(1, Decimal('2.50')), (4, Decimal('1.2'))])
        self.assertContains(odpowiedz, 'Do zapłaty: 8.00 zł')

    @patch('magazyn.services.zarejestruj_sprzedaz', side_effect=BrakNaStanie('Marchew: na stanie 1,00 kg'))
    def test_brak_na_stanie_zachowuje_pozycje(self, _):
        odpowiedz = self.sprzedaj(('2', '5'))
        self.assertContains(odpowiedz, 'Marchew: na stanie 1,00 kg')
        self.assertEqual(odpowiedz.context['formset'].total_form_count(), 1)

    @patch('magazyn.services.zarejestruj_sprzedaz')
    def test_bledne_masy_nie_trafiaja_do_logiki(self, zapis):
        for pozycje in [[], [('1', '-3')], [('1', '0')], [('1', '1'), ('1', '2')], [('999', '1')]]:
            self.assertEqual(self.sprzedaj(*pozycje).status_code, 200)
        zapis.assert_not_called()

    def test_zapis_bez_logiki_pokazuje_komunikat(self):
        odpowiedz = self.sprzedaj(('1', '1'))
        self.assertContains(odpowiedz, 'zarejestruj_sprzedaz nie ma jeszcze logiki')

    @patch('magazyn.services.zarejestruj_dostawe')
    def test_dostawa_wymaga_wszystkich_ilosci_i_przyjmuje_zero(self, zapis):
        pola = {f'p{w.produkt.id}': '0' for w in services.plan_na_dzien(timezone.localdate())}
        self.client.post('/admin/dostawa/', {**pola, 'p1': ''})
        zapis.assert_not_called()
        self.client.post('/admin/dostawa/', {**pola, 'p1': '-1'})
        zapis.assert_not_called()
        self.client.post('/admin/dostawa/', pola)
        zapis.assert_called_once()

    def test_dostawa_wczorajsza_wyroznia_za_mala_ilosc(self):
        wczoraj = timezone.localdate() - timedelta(days=1)
        odpowiedz = self.client.get(f'/admin/dostawa/?dzien={wczoraj.isoformat()}')
        self.assertContains(odpowiedz, 'class="za-malo"')

    @patch('magazyn.services.zarejestruj_ubytek', side_effect=BrakNaStanie('Na stanie 1,00 kg'))
    def test_ubytek_pokazuje_blad_przy_polu(self, _):
        odpowiedz = self.client.post('/admin/ubytek/', {'produkt': '1', 'masa_kg': '5'})
        self.assertContains(odpowiedz, 'Na stanie 1,00 kg')

    def test_niepoprawny_dzien_w_adresie(self):
        for dzien in ['zle', '2026-13-45', '0001-01-01', '9999-12-31']:
            self.assertEqual(self.client.get(f'/admin/sprzedaz/historia/?dzien={dzien}').status_code, 200)


class PanelProduktowTests(TestCase):
    def setUp(self):
        self.client.force_login(konto('wlasciciel', 'wlasciciel'))

    def nowy(self, **pola):
        return {
            'nazwa': 'Marchew',
            'odmiana': '',
            'standardowa_ilosc_kg': '30',
            'w_ofercie': 'on',
            'cena_za_kg': '2,50',
            'obowiazuje_od': '2026-11-05',
            **pola,
        }

    def test_tylko_dla_wlasciciela(self):
        self.client.force_login(konto('sprzedawca', 'sprzedawca'))
        for adres in ['/admin/produkty/', '/admin/produkty/nowy/', '/admin/produkty/1/']:
            self.assertEqual(self.client.get(adres).status_code, 403, adres)

    def test_lista_pokazuje_wycofane(self):
        self.assertContains(self.client.get('/admin/produkty/'), 'Szparagi')

    def test_nieznany_produkt(self):
        self.assertEqual(self.client.get('/admin/produkty/999/').status_code, 404)

    @patch('magazyn.services.dodaj_produkt')
    def test_nowy_produkt_wymaga_ceny(self, zapis):
        self.client.post('/admin/produkty/nowy/', self.nowy(cena_za_kg=''))
        zapis.assert_not_called()
        self.client.post('/admin/produkty/nowy/', self.nowy())
        self.assertEqual(zapis.call_args.kwargs['cena_za_kg'], Decimal('2.50'))

    @patch('magazyn.services.dodaj_produkt', side_effect=services.ProduktOdrzucony('Taki produkt już jest'))
    def test_odrzucony_produkt(self, _):
        self.assertContains(self.client.post('/admin/produkty/nowy/', self.nowy()), 'Taki produkt już jest')

    @patch('magazyn.services.zmien_cene')
    @patch('magazyn.services.zmien_produkt')
    def test_edycja_rozroznia_formularze(self, produkt, cena):
        self.client.post('/admin/produkty/1/', self.nowy())
        produkt.assert_called_once()
        self.assertTrue(produkt.call_args.kwargs['w_ofercie'])
        cena.assert_not_called()
        produkt.reset_mock()
        self.client.post('/admin/produkty/1/', {'zapisz_cene': '', 'cena_za_kg': '4,10', 'obowiazuje_od': '2026-11-05'})
        cena.assert_called_once()
        self.assertEqual(cena.call_args.args[0], 1)
        self.assertEqual(cena.call_args.kwargs['cena_za_kg'], Decimal('4.10'))
        produkt.assert_not_called()

    def test_wycofanie_z_oferty(self):
        with patch('magazyn.services.zmien_produkt') as zapis:
            pola = self.nowy()
            del pola['w_ofercie']
            self.client.post('/admin/produkty/1/', pola)
        self.assertFalse(zapis.call_args.kwargs['w_ofercie'])
