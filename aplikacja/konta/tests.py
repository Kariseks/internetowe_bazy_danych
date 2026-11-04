from unittest.mock import patch

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.urls import reverse

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
        self.assertRedirects(self.zaloguj(next=reverse('rejestracja')), reverse('rejestracja'))

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
