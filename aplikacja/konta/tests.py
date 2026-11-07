from decimal import Decimal
from unittest.mock import patch

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.urls import reverse

import atrapy
from magazyn.tests import konto

from . import powiadomienia, services
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


HASLO = 'Stare-Haslo-71'
ADRES = 'anna@example.com'


def nowy_klient():
    return get_user_model().objects.create_user(ADRES, ADRES, HASLO)


class LogowanieTests(TestCase):
    def setUp(self):
        self.klient = nowy_klient()
        sprzedawca = konto('sprzedawca', 'sprzedawca')
        sprzedawca.set_password(HASLO)
        sprzedawca.save()

    def zaloguj(self, login=ADRES, haslo=HASLO, strona='logowanie', **dane):
        return self.client.post(reverse(strona), {'username': login, 'password': haslo, **dane})

    def test_klient_trafia_do_katalogu(self):
        self.assertRedirects(self.zaloguj(), reverse('katalog'))

    def test_personel_nie_zaloguje_sie_w_panelu_klienta(self):
        poprawne = self.zaloguj('sprzedawca')
        bledne = self.zaloguj('sprzedawca', 'zle')
        self.assertContains(poprawne, 'Niepoprawny login lub hasło.')
        self.assertEqual(poprawne.context['form'].errors, bledne.context['form'].errors)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_personel_loguje_sie_w_panelu_administratora(self):
        odpowiedz = self.zaloguj('sprzedawca', strona='admin:login', next=reverse('admin:index'))
        self.assertRedirects(odpowiedz, reverse('admin:index'))

    def test_klient_nie_zaloguje_sie_w_panelu_administratora(self):
        self.assertEqual(self.zaloguj(strona='admin:login').status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_next_ma_pierwszenstwo(self):
        self.assertRedirects(self.zaloguj(next=reverse('moje_rezerwacje')), reverse('moje_rezerwacje'))

    def test_zalogowany_nie_widzi_formularza(self):
        self.client.force_login(self.klient)
        self.assertRedirects(self.client.get(reverse('logowanie')), reverse('katalog'))

    def test_bledne_haslo_i_nieaktywne_konto_daja_ten_sam_komunikat(self):
        bledne = self.zaloguj(haslo='zle')
        self.klient.is_active = False
        self.klient.save()
        nieaktywne = self.zaloguj()
        for odpowiedz in (bledne, nieaktywne):
            self.assertContains(odpowiedz, 'Niepoprawny login lub hasło.')
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_klient_nie_wejdzie_do_panelu_administratora(self):
        self.zaloguj()
        self.assertEqual(self.client.get(reverse('admin:index')).status_code, 302)

    def test_wylogowanie(self):
        self.client.force_login(self.klient)
        self.assertRedirects(self.client.post(reverse('wyloguj')), reverse('katalog'))
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_odnosniki_z_formularza_dzialaja(self):
        for nazwa in ('haslo_reset', 'rejestracja'):
            self.assertEqual(self.client.get(reverse(nazwa)).status_code, 200)


class ResetHaslaTests(TestCase):
    NOWE = 'Nowe-Haslo-82'

    def setUp(self):
        self.klient = nowy_klient()

    def popros(self, adres=ADRES):
        return self.client.post(reverse('haslo_reset'), {'email': adres}, follow=True)

    def link(self):
        return next(s for s in mail.outbox[-1].body.split() if s.startswith('http'))

    def formularz(self):
        odpowiedz = self.client.get(self.link(), follow=True)
        self.assertTrue(odpowiedz.context['validlink'])
        return odpowiedz.redirect_chain[-1][0]

    def test_logowanie_do_panelu_administratora_ma_odnosnik(self):
        self.assertContains(self.client.get(reverse('admin:login')), f'href="{reverse("haslo_reset")}"')

    def test_link_wazny_3_dni(self):
        self.assertEqual(settings.PASSWORD_RESET_TIMEOUT, 3 * 24 * 60 * 60)

    def test_caly_przebieg(self):
        self.assertContains(self.popros(), 'wysłaliśmy')
        self.assertEqual(mail.outbox[0].subject, 'Warzywniak: reset hasła')
        adres = self.formularz()
        odpowiedz = self.client.post(adres, {'new_password1': self.NOWE, 'new_password2': self.NOWE})
        self.assertRedirects(odpowiedz, reverse('haslo_zmienione'))
        self.assertContains(self.client.get(reverse('haslo_zmienione')), reverse('admin:login'))
        self.assertNotIn('_auth_user_id', self.client.session)
        self.klient.refresh_from_db()
        self.assertTrue(self.klient.check_password(self.NOWE))

    def test_link_dziala_raz(self):
        self.popros()
        self.client.post(self.formularz(), {'new_password1': self.NOWE, 'new_password2': self.NOWE})
        ponownie = self.client.get(self.link(), follow=True)
        self.assertContains(ponownie, 'Ten link wygasł albo został już użyty.')

    def test_nieznany_adres_i_nieaktywne_konto_bez_wiadomosci(self):
        self.klient.is_active = False
        self.klient.save()
        for adres in ('nikt@example.com', ADRES):
            self.assertContains(self.popros(adres), 'wysłaliśmy')
        self.assertEqual(mail.outbox, [])

    def test_haslo_musi_spelniac_reguly(self):
        self.popros()
        adres = self.formularz()
        for pierwsze, drugie in (('12345678', '12345678'), (self.NOWE, 'Inne-Haslo-93')):
            odpowiedz = self.client.post(adres, {'new_password1': pierwsze, 'new_password2': drugie})
            self.assertEqual(odpowiedz.status_code, 200)
            self.assertTrue(odpowiedz.context['form'].errors)
        self.klient.refresh_from_db()
        self.assertTrue(self.klient.check_password(HASLO))


class RejestracjaTests(TestCase):
    def dane(self, **pola):
        return {'imie': 'Anna', 'nazwisko': 'Kowalska', 'email': 'Anna@Example.com', 'telefon': '501 200 300',
                'haslo': 'Warzywa-2026!', 'haslo2': 'Warzywa-2026!', **pola}

    @patch('konta.services.zaloz_klienta')
    def test_konto_i_przejscie_do_karty(self, zapis):
        zapis.return_value = get_user_model().objects.create_user('zalozone@example.com')
        self.assertRedirects(self.client.post(reverse('rejestracja'), self.dane()), reverse('karta'))
        zapis.assert_called_once_with('Anna', 'Kowalska', 'anna@example.com', '501 200 300', 'Warzywa-2026!')
        self.assertEqual(self.client.session['nowe_konto'], zapis.return_value.pk)

    @patch('konta.services.zaloz_klienta')
    def test_bledne_dane(self, zapis):
        nowy_klient()
        for pola, blad in [
            ({'email': ADRES.upper()}, 'Konto z tym adresem e-mail już istnieje.'),
            ({'haslo2': 'Inne-Haslo-2026'}, 'Hasła nie są takie same.'),
            ({'haslo': '12345678', 'haslo2': '12345678'}, 'To hasło jest zbyt powszechne.'),
            ({'telefon': 'abc'}, 'Podaj numer telefonu'),
        ]:
            odpowiedz = self.client.post(reverse('rejestracja'), self.dane(**pola))
            self.assertContains(odpowiedz, blad)
            self.assertNotContains(odpowiedz, 'Warzywa-2026!')
        zapis.assert_not_called()

    def test_zapis_bez_logiki(self):
        self.assertContains(self.client.post(reverse('rejestracja'), self.dane(), follow=True), 'nic nie zapisano')

    def test_zalogowany_wraca_do_katalogu(self):
        self.client.force_login(nowy_klient())
        self.assertRedirects(self.client.get(reverse('rejestracja')), reverse('katalog'))


@patch('konta.services.zapisz_karte')
class KartaTests(TestCase):
    def nowe_konto(self):
        sesja = self.client.session
        sesja['nowe_konto'] = nowy_klient().pk
        sesja.save()

    def test_po_zalozeniu_konta(self, zapis):
        self.nowe_konto()
        odpowiedz = self.client.post(reverse('karta'), {'wynik': 'zatwierdz'}, follow=True)
        self.assertRedirects(odpowiedz, reverse('logowanie'))
        self.assertContains(odpowiedz, 'Konto założone')
        konto_id, identyfikator = zapis.call_args.args
        self.assertEqual(konto_id, get_user_model().objects.get(username=ADRES).pk)
        self.assertTrue(identyfikator.startswith('test_'))
        self.assertNotIn('nowe_konto', self.client.session)

    def test_przerwanie_zostawia_konto_bez_karty(self, zapis):
        self.nowe_konto()
        odpowiedz = self.client.post(reverse('karta'), {'wynik': 'przerwij'}, follow=True)
        self.assertContains(odpowiedz, 'Bez karty nie można składać rezerwacji.')
        self.assertContains(odpowiedz, 'Konto założone')
        zapis.assert_not_called()

    def test_klient_zmienia_karte(self, zapis):
        klient = nowy_klient()
        self.client.force_login(klient)
        self.assertRedirects(self.client.post(reverse('karta'), {'wynik': 'zatwierdz'}), reverse('konto'))
        self.assertEqual(zapis.call_args.args[0], klient.pk)

    def test_bez_konta_trafia_na_logowanie(self, zapis):
        self.assertRedirects(self.client.get(reverse('karta')), reverse('logowanie'))


class KontoKlientaTests(TestCase):
    def setUp(self):
        self.klient = nowy_klient()
        self.client.force_login(self.klient)

    @patch('konta.services.zmien_telefon')
    def test_zmiana_telefonu(self, zapis):
        self.assertRedirects(self.client.post(reverse('konto'), {'telefon': '600 100 200'}), reverse('konto'))
        zapis.assert_called_once_with(self.klient, '600 100 200')
        self.assertContains(self.client.post(reverse('konto'), {'telefon': '12'}), 'Podaj numer telefonu')

    def test_brak_karty(self):
        bez_karty = atrapy.profil_klienta(self.klient)
        bez_karty.identyfikator_karty = None
        with patch('konta.services.profil_klienta', return_value=bez_karty):
            self.assertContains(self.client.get(reverse('konto')), 'Zarejestruj kartę')
        odpowiedz = self.client.get(reverse('konto'))
        self.assertContains(odpowiedz, 'Zmień kartę')
        self.assertContains(odpowiedz, 'Konto może składać rezerwacje.')

    def test_zmiana_hasla(self):
        nowe = 'Nowe-Haslo-2026'
        odpowiedz = self.client.post(reverse('zmiana_hasla'), {'old_password': HASLO, 'new_password1': nowe, 'new_password2': nowe})
        self.assertRedirects(odpowiedz, reverse('konto'))
        self.klient.refresh_from_db()
        self.assertTrue(self.klient.check_password(nowe))


class PowiadomieniaTests(TestCase):
    def setUp(self):
        self.rezerwacja = atrapy.rezerwacja_klienta(None, 401)

    def wiadomosc(self):
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['kowalska@example.com'])
        return mail.outbox[0]

    def test_konto(self):
        powiadomienia.konto_zalozone(nowy_klient())
        self.assertEqual(mail.outbox[0].to, [ADRES])
        self.assertIn(f'adresem {ADRES}', mail.outbox[0].body)

    def test_rezerwacja(self):
        powiadomienia.rezerwacja(self.rezerwacja, 'zlozona')
        wiadomosc = self.wiadomosc()
        self.assertEqual(wiadomosc.subject, 'Warzywniak: rezerwacja złożona')
        self.assertIn('- Ziemniaki (Irys): 10 kg\n- Jabłka (Ligol): 4,5 kg', wiadomosc.body)
        self.assertIn('do 18:00, ', wiadomosc.body)

    def test_anulowanie_bez_pozycji(self):
        powiadomienia.rezerwacja(self.rezerwacja, 'anulowana')
        wiadomosc = self.wiadomosc()
        self.assertIn('anulowana bez opłaty', wiadomosc.body)
        self.assertNotIn('Ziemniaki', wiadomosc.body)

    def test_oplata_i_blokada(self):
        self.rezerwacja.oplata_za_nieodebranie = Decimal('9.00')
        powiadomienia.oplata(self.rezerwacja)
        self.assertIn('Opłata za nieodebranie: 9,00 zł', self.wiadomosc().body)
        self.assertNotIn('nie możesz składać', mail.outbox[0].body)
        self.rezerwacja.klient.zablokowany = True
        powiadomienia.oplata(self.rezerwacja)
        self.assertIn('nie możesz składać nowych rezerwacji', mail.outbox[1].body)

    def test_przypomnienie(self):
        powiadomienia.przypomnienie(self.rezerwacja, Decimal('5.99'))
        self.assertIn('naliczy opłatę 5,99 zł', self.wiadomosc().body)


class StronyBledowTests(TestCase):
    def test_404(self):
        odpowiedz = self.client.get('/nie-ma-takiej-strony/')
        self.assertEqual(odpowiedz.status_code, 404)
        self.assertContains(odpowiedz, 'Nie ma takiej strony', status_code=404)

    def test_403_dla_personelu_prowadzi_do_panelu(self):
        self.client.force_login(konto('sprzedawca', 'sprzedawca'))
        for strona in ['/konto/', '/admin/konta/']:
            odpowiedz = self.client.get(strona)
            self.assertContains(odpowiedz, 'Brak dostępu', status_code=403)
            self.assertContains(odpowiedz, 'href="/admin/"', status_code=403)
