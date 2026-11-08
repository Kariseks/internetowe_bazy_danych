from datetime import datetime, time, timedelta
from decimal import Decimal
from io import StringIO
from unittest.mock import patch

from django.core import mail
from django.core.management import call_command
from django.db import connection
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

import atrapy
from konta.tests import nowy_klient
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
        self.assertEqual(zapis.call_args.args[1], [(1, Decimal('9.95')), (2, Decimal(0))])
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
        self.assertEqual(zapis.call_args.args[2], Decimal(5))
        self.assertContains(odpowiedz, 'Zarezerwowano 40 kg')


def za_dni(n):
    return (timezone.localdate() + timedelta(days=n)).isoformat()


class PanelKlientaTests(TestCase):
    def setUp(self):
        self.klient = nowy_klient()
        self.client.force_login(self.klient)
        # Dzień bez rezerwacji klienta w atrapach (rezerwacja 401 jest za 2 dni).
        self.nowa = reverse('nowa_rezerwacja', args=[za_dni(3)])

    def strony(self):
        return [self.nowa, '/rezerwacje/', '/rezerwacje/401/zmien/', '/rezerwacje/401/anuluj/', '/konto/', '/konto/haslo/', '/zaleglosc/']

    def test_dostep(self):
        for strona in self.strony():
            self.assertEqual(self.client.get(strona).status_code, 200, strona)
        self.client.force_login(konto('sprzedawca', 'sprzedawca'))
        for strona in self.strony():
            self.assertEqual(self.client.get(strona).status_code, 403, strona)
        self.client.logout()
        for strona in self.strony():
            self.assertRedirects(self.client.get(strona), f'/logowanie/?next={strona}', fetch_redirect_response=False)

    def test_katalog_kieruje_niezalogowanego_na_logowanie(self):
        self.client.logout()
        odpowiedz = self.client.get(reverse('katalog'))
        self.assertContains(odpowiedz, f'/logowanie/?next={self.nowa}')
        self.assertNotContains(odpowiedz, f'href="{self.nowa}"')
        self.assertContains(self.client.get(reverse('katalog')), 'Załóż konto')

    def test_katalog_po_18_zamyka_jutro(self):
        jutro = reverse('nowa_rezerwacja', args=[za_dni(1)])
        self.assertContains(self.client.get(reverse('katalog')), f'href="{self.nowa}"')
        wieczor = timezone.make_aware(datetime.combine(timezone.localdate(), time(18, 0)))
        with patch('atrapy.teraz', return_value=wieczor):
            odpowiedz = self.client.get(reverse('katalog'))
        self.assertNotContains(odpowiedz, jutro)
        self.assertContains(odpowiedz, 'zamknięte')

    @patch('rezerwacje.services.zloz_rezerwacje')
    def test_formularz_rezerwacji(self, zapis):
        for pola, blad in [
            ({'p1': '15', 'p2': '5,5'}, 'najwyżej 20 kg, a ma 20,5 kg'),
            ({'p1': '0,05'}, 'cyfr'),
            ({}, 'Wpisz ilość co najmniej jednego produktu.'),
            ({'p1': '0'}, 'Wpisz ilość co najmniej jednego produktu.'),
            ({'p9': '19'}, 'Dostępne:'),
        ]:
            self.assertContains(self.client.post(self.nowa, pola), blad)
        zapis.assert_not_called()
        self.assertRedirects(self.client.post(self.nowa, {'p1': '12,5', 'p8': '7,5', 'p2': ''}), reverse('moje_rezerwacje'))
        zapis.assert_called_once_with(self.klient, timezone.localdate() + timedelta(days=3), [(1, Decimal('12.5')), (8, Decimal('7.5'))])

    @patch('rezerwacje.services.zloz_rezerwacje', side_effect=services.RezerwacjaOdrzucona('Dostępne już tylko 2 kg'))
    def test_odrzucenie_zostawia_ilosci(self, _):
        odpowiedz = self.client.post(self.nowa, {'p1': '5'})
        self.assertContains(odpowiedz, 'Dostępne już tylko 2 kg')
        self.assertContains(odpowiedz, 'value="5"')

    def test_zapis_bez_logiki(self):
        self.assertContains(self.client.post(self.nowa, {'p1': '5'}, follow=True), 'nic nie zapisano')

    def test_przeszkody(self):
        istniejaca = atrapy.rezerwacja_klienta(None, 401)
        for przeszkoda, tekst in [
            (atrapy.Atrapa(powod='karta', rezerwacja=None, zaleglosc=None), 'href="/konto/"'),
            (atrapy.Atrapa(powod='zaleglosc', rezerwacja=None, zaleglosc=Decimal('123.40')), '123,40 zł'),
            (atrapy.Atrapa(powod='istnieje', rezerwacja=istniejaca, zaleglosc=None), '/rezerwacje/401/zmien/'),
        ]:
            with patch('rezerwacje.services.przeszkoda', return_value=przeszkoda):
                odpowiedz = self.client.get(self.nowa)
            self.assertContains(odpowiedz, tekst)
            self.assertNotContains(odpowiedz, 'Zarezerwuj</button>')
        self.assertContains(self.client.get(reverse('nowa_rezerwacja', args=[za_dni(0)])), 'zakończyło się')

    def test_nieznana_albo_cudza_rezerwacja(self):
        for strona in ['/rezerwacje/999/zmien/', '/rezerwacje/999/anuluj/', '/rezerwacje/nowa/jutro/', '/rezerwacje/nowa/2026-13-40/']:
            self.assertEqual(self.client.get(strona).status_code, 404, strona)

    def test_moje_rezerwacje(self):
        odpowiedz = self.client.get('/rezerwacje/')
        self.assertContains(odpowiedz, '/rezerwacje/401/zmien/')
        self.assertContains(odpowiedz, '/rezerwacje/401/anuluj/')
        self.assertNotContains(odpowiedz, '/rezerwacje/402/')
        self.assertEqual([r.id for r in odpowiedz.context['zakonczone']], [403, 404, 405])

    def test_zmiana_wypelnia_ilosci(self):
        self.assertContains(self.client.get('/rezerwacje/401/zmien/'), 'value="10,0"')

    @patch('rezerwacje.services.zmien_rezerwacje')
    def test_zmiana(self, zapis):
        self.assertRedirects(self.client.post('/rezerwacje/401/zmien/', {'p1': '3'}), reverse('moje_rezerwacje'))
        zapis.assert_called_once_with(self.klient, 401, [(1, Decimal(3))])

    @patch('rezerwacje.services.anuluj_rezerwacje')
    def test_anulowanie(self, zapis):
        self.assertContains(self.client.get('/rezerwacje/401/anuluj/'), 'Anuluj rezerwację')
        self.assertRedirects(self.client.post('/rezerwacje/401/anuluj/'), reverse('moje_rezerwacje'))
        zapis.assert_called_once_with(self.klient, 401)

    @patch('rezerwacje.services.anuluj_rezerwacje')
    def test_po_terminie_nie_ma_zmian(self, zapis):
        for strona in ['/rezerwacje/402/zmien/', '/rezerwacje/402/anuluj/']:
            odpowiedz = self.client.post(strona, {'p1': '3'}, follow=True)
            self.assertRedirects(odpowiedz, reverse('moje_rezerwacje'))
            self.assertContains(odpowiedz, 'nie można już zmienić ani anulować')
        zapis.assert_not_called()


class PrzypomnieniaTests(TestCase):
    """PU31 na atrapach: dziś 101 i 103 są złożone, 102 przygotowana, 104 odebrana."""

    def uruchom(self):
        wyjscie, bledy = StringIO(), StringIO()
        call_command('wyslij_przypomnienia', stdout=wyjscie, stderr=bledy)
        return wyjscie.getvalue(), bledy.getvalue()

    def test_tylko_rezerwacje_do_odbioru(self):
        wyjscie, bledy = self.uruchom()
        self.assertEqual(sorted(m.to[0] for m in mail.outbox), [
            'kowalska@example.com', 'wisniewski@example.com', 'zielinska@example.com',
        ])
        self.assertIn('Wysłano przypomnień: 3.', wyjscie)
        self.assertEqual(bledy, '')

    def test_tresc_z_oplata(self):
        self.uruchom()
        tresc = next(m.body for m in mail.outbox if m.to == ['kowalska@example.com'])
        # 10 kg × 3,20 zł + 3,5 kg × 3,80 zł = 45,30 zł, opłata 10%.
        self.assertIn('naliczy opłatę 4,53 zł', tresc)
        self.assertIn('Ziemniaki (Irys): 10 kg', tresc)

    def test_blad_jednej_wiadomosci_nie_zatrzymuje_pozostalych(self):
        with patch('konta.powiadomienia.send_mail', side_effect=[OSError('brak połączenia'), 1, 1]) as wysylka, \
                self.assertLogs('rezerwacje.services', 'ERROR'):
            wyjscie, bledy = self.uruchom()
        self.assertEqual(wysylka.call_count, 3)
        self.assertIn('Wysłano przypomnień: 2.', wyjscie)
        self.assertIn('rezerwacjach: 101.', bledy)


class NaglowekTests(TestCase):
    def test_menu_klienta_z_biezaca_strona(self):
        self.client.force_login(nowy_klient())
        odpowiedz = self.client.get('/rezerwacje/')
        self.assertContains(odpowiedz, 'aria-controls="menu"')
        self.assertContains(odpowiedz, 'href="/rezerwacje/" aria-current="page"')
        self.assertNotContains(odpowiedz, 'href="/zaleglosc/" aria-current')

    def test_bez_menu_bocznego_dla_niezalogowanego(self):
        odpowiedz = self.client.get('/')
        self.assertNotContains(odpowiedz, 'class="burger"')
        self.assertNotContains(odpowiedz, 'menu.js')
