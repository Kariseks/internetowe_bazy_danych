"""Testy akceptacyjne przypadków użycia: plan w sprawozdaniu, tab. „Plan testów akceptacyjnych” (p. 10.2).

Każdy test tworzy stan początkowy funkcjami zapisu z services.py, wykonuje przypadek użycia przez strony aplikacji
(klient testowy Django) i sprawdza stan po nim funkcjami odczytu z services.py. Nie zależą więc od nazw modeli.
Dopóki services.py ma stuby, testy kończą się błędem NotImplementedError.

Zegar jest zamrożony na dniu D (patch django.utils.timezone.now), dlatego logika bierze czas z django.utils.timezone.
"""
import threading
from contextlib import contextmanager
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core import mail
from django.core.mail.backends.base import BaseEmailBackend
from django.core.management import call_command
from django.db import connection
from django.test import Client, TestCase, TransactionTestCase
from django.utils import timezone

from konta import services as konta
from magazyn import services as magazyn
from magazyn.tests import konto
from rezerwacje import services as rezerwacje
from rozliczenia import services as rozliczenia

D = date(2026, 11, 16)
HASLO = 'Warzywa-2026!'
NOWE_HASLO = 'Nowe-Haslo-2026'


class Dane:
    """Zegar na dniu D i pomocnicze funkcje stanu początkowego."""

    def setUp(self):
        zegar = patch('django.utils.timezone.now')
        self.teraz = zegar.start()
        self.addCleanup(zegar.stop)
        self.ustaw_zegar(0, '10:00')
        self.numer = 0
        self.sprzedawca = konto('sprzedawca', 'sprzedawca')
        self.wlasciciel = konto('wlasciciel', 'wlasciciel')
        self.ziemniaki = self.produkt('Ziemniaki', '3.20')
        self.marchew = self.produkt('Marchew', '4.00')

    # Zegar

    def dzien(self, dni):
        return D + timedelta(days=dni)

    def ustaw_zegar(self, dni, godzina):
        h, m = map(int, godzina.split(':'))
        self.teraz.return_value = timezone.make_aware(datetime.combine(self.dzien(dni), time(h, m)))

    @contextmanager
    def o_godzinie(self, dni, godzina='10:00'):
        poprzednia = self.teraz.return_value
        self.ustaw_zegar(dni, godzina)
        try:
            yield
        finally:
            self.teraz.return_value = poprzednia

    # Stan początkowy

    def kolejny(self):
        self.numer += 1
        return self.numer

    def produkt(self, nazwa, cena):
        """Produkt w ofercie, standardowa dzienna ilość (czyli plan) 100 kg."""
        return magazyn.dodaj_produkt(nazwa, '', Decimal(100), True, Decimal(cena), D - timedelta(days=60))

    def klient(self, email=None, karta=True):
        n = self.kolejny()
        uzytkownik = konta.zaloz_klienta('Anna', f'Testowa{n}', email or f'klient{n}@example.com', f'500 000 {n:03}', HASLO)
        if karta:
            konta.zapisz_karte(uzytkownik.pk, f'test_{n}')
        return uzytkownik

    def zarezerwuj(self, klient, dni, *pozycje):
        """Rezerwacja na D+dni złożona dwa dni wcześniej, więc przed terminem."""
        with self.o_godzinie(dni - 2):
            return rezerwacje.zloz_rezerwacje(klient, self.dzien(dni), [(p.id, Decimal(kg)) for p, kg in pozycje])

    def zarezerwowano(self, produkt, dni, kg):
        """Ilość zarezerwowana przez innych klientów, po 18 kg na rezerwację."""
        while kg > 0:
            czesc = min(kg, 18)
            self.zarezerwuj(self.klient(), dni, (produkt, czesc))
            kg -= czesc

    def dostawa(self, dni, *pozycje):
        with self.o_godzinie(dni, '05:40'):
            magazyn.zarejestruj_dostawe(self.dzien(dni), [(p.id, Decimal(kg)) for p, kg in pozycje], self.sprzedawca)

    def zaleglosc(self, klient, kwota, dni):
        """Opłata `kwota` za nieodebraną rezerwację na D+dni: 10 kg produktu po `kwota` zł/kg, czyli 10% wartości."""
        produkt = self.produkt(f'Produkt {self.kolejny()}', kwota)
        self.zarezerwuj(klient, dni, (produkt, 10))
        with self.o_godzinie(dni, '18:00'):
            call_command('oznacz_nieodebrane')

    # Odczyt stanu

    def dostepne(self, produkt, dni):
        return next(w.dostepne_kg for w in rezerwacje.oferta_na_dzien(self.dzien(dni)) if w.produkt.id == produkt.id)

    def stan(self, produkt):
        return next(w.stan_kg for w in magazyn.stan_produktow() if w.produkt.id == produkt.id)

    def jedyna_rezerwacja(self, klient):
        lista = rezerwacje.rezerwacje_klienta(klient)
        self.assertEqual(len(lista), 1)
        return lista[0]

    def zaleglosc_klienta(self, klient):
        return rozliczenia.zaleglosc_klienta(klient).zaleglosc

    def komunikaty(self, odpowiedz):
        return ' '.join(str(m) for m in odpowiedz.context['messages'])

    def adresaci(self):
        return [m.to[0] for m in mail.outbox]

    # Działania na stronach

    def zaloguj(self, uzytkownik):
        self.client.force_login(uzytkownik)

    def zarezerwuj_na_stronie(self, dni, **ilosci):
        return self.client.post(f'/rezerwacje/nowa/{self.dzien(dni).isoformat()}/', ilosci, follow=True)

    def pole(self, produkt):
        return f'p{produkt.id}'


class Akceptacja(Dane, TestCase):
    pass


class ZalozKontoTests(Akceptacja):
    """PU2 Załóż konto klienta."""

    ADRES = 'anna@example.com'

    def zaloz(self, **pola):
        dane = {'imie': 'Anna', 'nazwisko': 'Kowalska', 'email': self.ADRES, 'telefon': '501 200 300',
                'haslo': HASLO, 'haslo2': HASLO, **pola}
        return self.client.post('/rejestracja/', dane, follow=True)

    def konto_klienta(self):
        return next((k for k in konta.lista_kont() if k.email == self.ADRES), None)

    def test_ta01_konto_z_karta(self):
        self.zaloz()
        odpowiedz = self.client.post('/konto/karta/', {'wynik': 'zatwierdz'}, follow=True)
        uzytkownik = self.konto_klienta()
        self.assertEqual(uzytkownik.rola, 'klient')
        self.assertEqual(uzytkownik.username, self.ADRES)
        self.assertTrue(konta.profil_klienta(uzytkownik).identyfikator_karty)
        self.assertEqual(self.adresaci(), [self.ADRES])
        self.assertTemplateUsed(odpowiedz, 'konta/logowanie.html')
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_ta02_zajety_adres_albo_slabe_haslo(self):
        self.klient(self.ADRES)
        liczba = len(konta.lista_kont())
        zajety = self.zaloz()
        self.assertContains(zajety, 'Konto z tym adresem e-mail już istnieje.')
        slabe = self.zaloz(email='inna@example.com', haslo='12345678', haslo2='12345678')
        self.assertTrue(slabe.context['form'].errors['haslo'])
        for odpowiedz in (zajety, slabe):
            self.assertNotContains(odpowiedz, HASLO)
        self.assertEqual(len(konta.lista_kont()), liczba)

    def test_ta03_przerwana_karta(self):
        self.zaloz()
        odpowiedz = self.client.post('/konto/karta/', {'wynik': 'przerwij'}, follow=True)
        self.assertIsNone(konta.profil_klienta(self.konto_klienta()).identyfikator_karty)
        self.assertContains(odpowiedz, 'Bez karty nie można składać rezerwacji.')


class ZalogujSieTests(Akceptacja):
    """PU3 Zaloguj się."""

    def setUp(self):
        super().setUp()
        self.anna = self.klient('anna@example.com')
        self.sprzedawca.set_password(HASLO)
        self.sprzedawca.save()

    def zaloguj_w(self, strona, login, haslo=HASLO):
        self.client.logout()
        return self.client.post(strona, {'username': login, 'password': haslo, 'next': '/admin/'}, follow=True)

    def test_ta04_kazda_rola_w_swoim_panelu(self):
        klient = self.client.post('/logowanie/', {'username': 'anna@example.com', 'password': HASLO}, follow=True)
        self.assertRedirects(klient, '/')
        self.assertEqual(int(self.client.session['_auth_user_id']), self.anna.pk)
        sprzedawca = self.zaloguj_w('/admin/login/', 'sprzedawca')
        self.assertRedirects(sprzedawca, '/admin/')
        self.assertEqual(int(self.client.session['_auth_user_id']), self.sprzedawca.pk)

    def test_ta05_ten_sam_komunikat(self):
        nieaktywny = self.klient('ola@example.com')
        konta.ustaw_aktywnosc(nieaktywny.pk, False)
        for strona, login, haslo in [
            ('/logowanie/', 'anna@example.com', 'zle-haslo'),
            ('/logowanie/', 'ola@example.com', HASLO),
            ('/logowanie/', 'sprzedawca', HASLO),
            ('/admin/login/', 'anna@example.com', HASLO),
        ]:
            odpowiedz = self.zaloguj_w(strona, login, haslo)
            if strona == '/logowanie/':
                self.assertContains(odpowiedz, 'Niepoprawny login lub hasło.')
            self.assertNotIn('_auth_user_id', self.client.session, (strona, login))


class ZresetujHasloTests(Akceptacja):
    """PU4 Zresetuj hasło."""

    ADRES = 'anna@example.com'

    def setUp(self):
        super().setUp()
        self.anna = self.klient(self.ADRES)
        mail.outbox.clear()

    def popros(self, adres=ADRES):
        return self.client.post('/haslo/reset/', {'email': adres}, follow=True)

    def link(self):
        return next(s for s in mail.outbox[-1].body.split() if s.startswith('http'))

    def otworz_link(self):
        return self.client.get(self.link(), follow=True)

    def ustaw_haslo(self, odpowiedz, haslo, powtorzenie=None):
        adres = odpowiedz.redirect_chain[-1][0]
        return self.client.post(adres, {'new_password1': haslo, 'new_password2': powtorzenie or haslo}, follow=True)

    def test_ta06_caly_przebieg(self):
        self.assertContains(self.popros(), 'wysłaliśmy')
        self.assertEqual(self.adresaci(), [self.ADRES])
        self.ustaw_haslo(self.otworz_link(), NOWE_HASLO)
        self.assertTrue(self.client.login(username=self.ADRES, password=NOWE_HASLO))
        self.assertFalse(self.client.login(username=self.ADRES, password=HASLO))
        self.client.logout()
        self.assertContains(self.otworz_link(), 'Ten link wygasł albo został już użyty.')

    def test_ta07_nieznany_albo_nieaktywny_adres(self):
        nieaktywny = self.klient('ola@example.com')
        konta.ustaw_aktywnosc(nieaktywny.pk, False)
        mail.outbox.clear()
        for adres in ('nikt@example.com', 'ola@example.com'):
            self.assertContains(self.popros(adres), 'wysłaliśmy')
        self.assertEqual(mail.outbox, [])

    def test_ta08_link_uzyty_albo_wygasly(self):
        self.popros()
        self.ustaw_haslo(self.otworz_link(), NOWE_HASLO)
        self.assertContains(self.otworz_link(), 'Ten link wygasł albo został już użyty.')
        self.popros()
        za_4_dni = datetime.now() + timedelta(days=4)
        with patch.object(PasswordResetTokenGenerator, '_now', return_value=za_4_dni):
            self.assertContains(self.otworz_link(), 'Ten link wygasł albo został już użyty.')
        self.assertTrue(self.client.login(username=self.ADRES, password=NOWE_HASLO))

    def test_ta09_haslo_niezgodne_z_regulami(self):
        self.popros()
        formularz = self.otworz_link()
        for haslo, powtorzenie in (('12345678', '12345678'), (NOWE_HASLO, 'Inne-Haslo-2026')):
            odpowiedz = self.ustaw_haslo(formularz, haslo, powtorzenie)
            self.assertTrue(odpowiedz.context['form'].errors)
        self.anna.refresh_from_db()
        self.assertTrue(self.anna.check_password(HASLO))  # login() zmieniłby last_login i unieważnił link
        self.ustaw_haslo(self.otworz_link(), NOWE_HASLO)
        self.assertTrue(self.client.login(username=self.ADRES, password=NOWE_HASLO))


class ZlozRezerwacjeTests(Akceptacja):
    """PU8 Złóż rezerwację. Plan ziemniaków na D+2: 100 kg, zarezerwowano 90 kg."""

    def setUp(self):
        super().setUp()
        self.zarezerwowano(self.ziemniaki, 2, 90)
        self.anna = self.klient('anna@example.com')
        mail.outbox.clear()

    def test_ta10_rezerwacja_zmniejsza_dostepne(self):
        self.zaloguj(self.anna)
        self.assertEqual(self.dostepne(self.ziemniaki, 2), 10)
        odpowiedz = self.zarezerwuj_na_stronie(2, **{self.pole(self.ziemniaki): '8'})
        self.assertRedirects(odpowiedz, '/rezerwacje/')
        rezerwacja = self.jedyna_rezerwacja(self.anna)
        self.assertEqual(rezerwacja.stan, 'zlozona')
        self.assertEqual([(p.produkt.id, p.ilosc_kg) for p in rezerwacja.pozycje], [(self.ziemniaki.id, 8)])
        self.assertEqual(self.dostepne(self.ziemniaki, 2), 2)
        self.assertEqual(self.adresaci(), ['anna@example.com'])

    def test_ta11_brak_karty_albo_zaleglosc(self):
        bez_karty = self.klient(karta=False)
        dluznik = self.klient()
        self.zaleglosc(dluznik, '100.00', -4)
        self.zaleglosc(dluznik, '0.01', -2)
        na_granicy = self.klient()
        self.zaleglosc(na_granicy, '100.00', -2)
        nowa = f'/rezerwacje/nowa/{self.dzien(2).isoformat()}/'
        for klient, tekst in [(bez_karty, 'potrzebna jest zarejestrowana karta'), (dluznik, '100,01 zł')]:
            self.zaloguj(klient)
            self.assertContains(self.client.get(nowa), tekst)
            self.zarezerwuj_na_stronie(2, **{self.pole(self.ziemniaki): '1'})
            self.assertEqual(
                [r for r in rezerwacje.rezerwacje_klienta(klient) if r.dzien_odbioru == self.dzien(2)], []
            )
        self.zaloguj(na_granicy)
        self.assertContains(self.client.get(nowa), 'id="form-rezerwacja"')

    def test_ta12_istniejaca_rezerwacja_na_dzien(self):
        istniejaca = self.zarezerwuj(self.anna, 2, (self.marchew, 2))
        self.zaloguj(self.anna)
        odpowiedz = self.client.get(f'/rezerwacje/nowa/{self.dzien(2).isoformat()}/')
        self.assertContains(odpowiedz, f'/rezerwacje/{istniejaca.id}/zmien/')
        self.jedyna_rezerwacja(self.anna)

    def test_ta13_ponad_dostepne_albo_ponad_20_kg(self):
        self.zaloguj(self.anna)
        ponad_dostepne = self.zarezerwuj_na_stronie(2, **{self.pole(self.ziemniaki): '11'})
        self.assertIn('10', str(ponad_dostepne.context['form'].errors[self.pole(self.ziemniaki)]))
        self.assertContains(ponad_dostepne, 'value="11"')
        ponad_limit = self.zarezerwuj_na_stronie(2, **{self.pole(self.ziemniaki): '10', self.pole(self.marchew): '11'})
        self.assertContains(ponad_limit, 'najwyżej 20 kg')
        self.assertEqual(rezerwacje.rezerwacje_klienta(self.anna), [])

    def test_ta15_po_18(self):
        self.zaloguj(self.anna)
        nowa = f'/rezerwacje/nowa/{self.dzien(1).isoformat()}/'
        self.ustaw_zegar(0, '17:59')
        self.assertContains(self.client.get(nowa), 'id="form-rezerwacja"')
        self.ustaw_zegar(0, '18:00')
        self.assertContains(self.client.get(nowa), 'zakończyło się')
        self.assertContains(self.zarezerwuj_na_stronie(1, **{self.pole(self.ziemniaki): '1'}), 'zakończyło się')
        self.assertEqual(rezerwacje.rezerwacje_klienta(self.anna), [])


class JednoczesneRezerwacjeTests(Dane, TransactionTestCase):
    """PU8 A3 i A5: dwa połączenia z bazą naraz, dlatego bez transakcji obejmującej cały test."""

    def setUp(self):
        super().setUp()
        self.zarezerwowano(self.ziemniaki, 2, 90)

    def w_watku(self, praca):
        def opakowana():
            try:
                praca()
            finally:
                connection.close()
        watek = threading.Thread(target=opakowana)
        watek.start()
        return watek

    def test_ta14_dwie_jednoczesne_rezerwacje(self):
        klienci = [self.klient(), self.klient()]
        start = threading.Barrier(2)

        def rezerwuj(klient):
            przegladarka = Client()
            przegladarka.force_login(klient)
            start.wait()
            przegladarka.post(f'/rezerwacje/nowa/{self.dzien(2).isoformat()}/', {self.pole(self.ziemniaki): '10'})

        for watek in [self.w_watku(lambda k=k: rezerwuj(k)) for k in klienci]:
            watek.join()
        przyjete = sum(len(rezerwacje.rezerwacje_klienta(k)) for k in klienci)
        self.assertEqual(przyjete, 1)
        self.assertEqual(self.dostepne(self.ziemniaki, 2), 0)

    def test_ta16_przekroczony_czas_blokady(self):
        anna = self.klient()
        rezerwacje.ustaw_plan(self.ziemniaki.id, self.dzien(2), Decimal(100))
        zablokowano, zwolnij = threading.Event(), threading.Event()

        def trzymaj_blokade():
            from django.db import transaction
            with transaction.atomic():
                rezerwacje.ustaw_plan(self.ziemniaki.id, self.dzien(2), Decimal(100))
                zablokowano.set()
                zwolnij.wait(10)

        watek = self.w_watku(trzymaj_blokade)
        self.assertTrue(zablokowano.wait(10))
        with connection.cursor() as kursor:
            kursor.execute('SET SESSION innodb_lock_wait_timeout = 1')
        try:
            self.client.force_login(anna)
            odpowiedz = self.zarezerwuj_na_stronie(2, **{self.pole(self.ziemniaki): '8'})
        finally:
            zwolnij.set()
            watek.join()
            with connection.cursor() as kursor:
                kursor.execute('SET SESSION innodb_lock_wait_timeout = DEFAULT')
        self.assertTrue(odpowiedz.context['form'].non_field_errors())
        self.assertContains(odpowiedz, 'value="8"')
        self.assertEqual(rezerwacje.rezerwacje_klienta(anna), [])


class AnulujRezerwacjeTests(Akceptacja):
    """PU10 Anuluj rezerwację."""

    def setUp(self):
        super().setUp()
        self.anna = self.klient('anna@example.com')

    def test_ta17_anulowanie_zwalnia_ilosc(self):
        self.zarezerwowano(self.ziemniaki, 2, 90)
        rezerwacja = self.zarezerwuj(self.anna, 2, (self.ziemniaki, 8))
        mail.outbox.clear()
        self.assertEqual(self.dostepne(self.ziemniaki, 2), 2)
        self.zaloguj(self.anna)
        self.client.post(f'/rezerwacje/{rezerwacja.id}/anuluj/')
        self.assertEqual(self.jedyna_rezerwacja(self.anna).stan, 'anulowana')
        self.assertEqual(self.dostepne(self.ziemniaki, 2), 10)
        self.assertEqual(self.adresaci(), ['anna@example.com'])

    def test_ta18_po_terminie(self):
        rezerwacja = self.zarezerwuj(self.anna, 1, (self.ziemniaki, 8))
        self.ustaw_zegar(0, '18:00')
        self.zaloguj(self.anna)
        odpowiedz = self.client.get(f'/rezerwacje/{rezerwacja.id}/anuluj/', follow=True)
        self.assertContains(odpowiedz, 'nie można już zmienić ani anulować')
        self.assertEqual(self.jedyna_rezerwacja(self.anna).stan, 'zlozona')
        self.assertNotContains(self.client.get('/rezerwacje/'), f'/rezerwacje/{rezerwacja.id}/anuluj/')


class ZarejestrujKarteTests(Akceptacja):
    """PU13 Zarejestruj kartę płatniczą."""

    def setUp(self):
        super().setUp()
        self.bez_karty = self.klient(karta=False)
        self.z_karta = self.klient()
        self.stara = konta.profil_klienta(self.z_karta).identyfikator_karty

    def karta(self, klient, wynik):
        self.zaloguj(klient)
        return self.client.post('/konto/karta/', {'wynik': wynik}, follow=True)

    def test_ta19_nowa_albo_zastepcza_karta(self):
        self.assertContains(self.karta(self.bez_karty, 'zatwierdz'), 'Konto może składać rezerwacje.')
        self.assertTrue(konta.profil_klienta(self.bez_karty).identyfikator_karty)
        self.karta(self.z_karta, 'zatwierdz')
        nowa = konta.profil_klienta(self.z_karta).identyfikator_karty
        self.assertTrue(nowa)
        self.assertNotEqual(nowa, self.stara)

    def test_ta20_przerwanie(self):
        for klient in (self.bez_karty, self.z_karta):
            self.assertContains(self.karta(klient, 'przerwij'), 'Nie zarejestrowano karty.')
        self.assertIsNone(konta.profil_klienta(self.bez_karty).identyfikator_karty)
        self.assertEqual(konta.profil_klienta(self.z_karta).identyfikator_karty, self.stara)


class PrzyjecieDostawyTests(Akceptacja):
    """PU14 Zarejestruj przyjęcie dostawy. Plan na D: 100 kg każdego produktu, stan ziemniaków 5 kg."""

    def setUp(self):
        super().setUp()
        self.dostawa(-1, (self.ziemniaki, 5))
        self.zaloguj(self.sprzedawca)

    def przyjmij(self, **zmiany):
        dane = {self.pole(w.produkt): str(w.plan_kg) for w in magazyn.plan_na_dzien(D)}
        return self.client.post('/admin/dostawa/', {**dane, **zmiany}, follow=True)

    def test_ta21_dostawa_zwieksza_stan(self):
        self.przyjmij(**{self.pole(self.ziemniaki): '98'})
        self.assertEqual(self.stan(self.ziemniaki), Decimal(103))
        pozycja = next(p for p in magazyn.dostawa_na_dzien(D).pozycje if p.produkt.id == self.ziemniaki.id)
        self.assertEqual(pozycja.roznica_kg, Decimal(-2))

    def test_ta22_bledna_ilosc(self):
        for ilosc in ('-1', '2,345'):
            odpowiedz = self.przyjmij(**{self.pole(self.ziemniaki): ilosc})
            self.assertTrue(odpowiedz.context['form'].errors[self.pole(self.ziemniaki)])
        self.assertIsNone(magazyn.dostawa_na_dzien(D))
        self.assertEqual(self.stan(self.ziemniaki), Decimal(5))

    def test_ta23_mniej_niz_zarezerwowano(self):
        self.zarezerwowano(self.ziemniaki, 0, 90)
        odpowiedz = self.przyjmij(**{self.pole(self.ziemniaki): '85'})
        self.assertContains(odpowiedz, 'class="za-malo"')
        pozycja = next(p for p in magazyn.dostawa_na_dzien(D).pozycje if p.produkt.id == self.ziemniaki.id)
        self.assertTrue(pozycja.za_malo)


class SprzedazTests(Akceptacja):
    """PU15 Zarejestruj sprzedaż. Stan ziemniaków 10 kg po 3,20 zł/kg, marchwi 20 kg."""

    def setUp(self):
        super().setUp()
        self.dostawa(-1, (self.ziemniaki, 10), (self.marchew, 20))
        self.zaloguj(self.sprzedawca)

    def sprzedaj(self, *pozycje):
        dane = {'form-TOTAL_FORMS': str(len(pozycje)), 'form-INITIAL_FORMS': '0'}
        for i, (produkt, masa) in enumerate(pozycje):
            dane[f'form-{i}-produkt'] = produkt.id
            dane[f'form-{i}-masa_kg'] = masa
        return self.client.post('/admin/sprzedaz/', dane, follow=True)

    def test_ta24_sprzedaz_zmniejsza_stan(self):
        self.sprzedaj((self.ziemniaki, '2,5'))
        sprzedaz, = magazyn.historia_sprzedazy(D, D)
        self.assertEqual(sprzedaz.suma, Decimal('8.00'))
        self.assertEqual([(p.masa_kg, p.cena_za_kg) for p in sprzedaz.pozycje], [(Decimal('2.5'), Decimal('3.20'))])
        self.assertEqual(self.stan(self.ziemniaki), Decimal('7.5'))

    def test_ta25_ponad_stan(self):
        odpowiedz = self.sprzedaj((self.ziemniaki, '12'), (self.marchew, '1'))
        self.assertIn('10', self.komunikaty(odpowiedz))
        self.assertEqual(odpowiedz.context['formset'].total_form_count(), 2)
        self.assertEqual(magazyn.historia_sprzedazy(D, D), [])
        self.assertEqual((self.stan(self.ziemniaki), self.stan(self.marchew)), (Decimal(10), Decimal(20)))


class RezerwacjaNaDzisTests(Akceptacja):
    """Rezerwacja Anny na D: 8 kg ziemniaków i 2 kg marchwi; dostawa na D: 50 kg ziemniaków, 20 kg marchwi."""

    def setUp(self):
        super().setUp()
        self.anna = self.klient('anna@example.com')
        self.rezerwacja = self.zarezerwuj(self.anna, 0, (self.ziemniaki, 8), (self.marchew, 2))
        self.dostawa(0, (self.ziemniaki, 50), (self.marchew, 20))
        self.zaloguj(self.sprzedawca)

    def przygotuj(self, ziemniaki, marchew, dalej=''):
        return self.client.post(
            f'/admin/rezerwacje/{self.rezerwacja.id}/przygotuj/{dalej}',
            {self.pole(self.ziemniaki): ziemniaki, self.pole(self.marchew): marchew},
            follow=True,
        )

    def masy(self):
        return {p.produkt.id: p.masa_odwazona_kg for p in rezerwacje.rezerwacja(self.rezerwacja.id).pozycje}


class PrzygotujRezerwacjeTests(RezerwacjaNaDzisTests):
    """PU20 Przygotuj rezerwację do odbioru."""

    def test_ta26_masy_i_stan(self):
        self.przygotuj('8,05', '1,95')
        self.assertEqual(rezerwacje.rezerwacja(self.rezerwacja.id).stan, 'przygotowana')
        self.assertEqual(self.masy(), {self.ziemniaki.id: Decimal('8.05'), self.marchew.id: Decimal('1.95')})

    def test_ta27_masa_zero(self):
        self.przygotuj('8,05', '0')
        self.assertEqual(rezerwacje.rezerwacja(self.rezerwacja.id).stan, 'przygotowana')
        self.assertEqual(self.masy(), {self.ziemniaki.id: Decimal('8.05'), self.marchew.id: Decimal(0)})


class WydajRezerwacjeTests(RezerwacjaNaDzisTests):
    """PU21 Wydaj rezerwację."""

    def wydanie(self):
        return f'/admin/rezerwacje/{self.rezerwacja.id}/wydaj/'

    def test_ta28_wydanie_przygotowanej(self):
        self.przygotuj('8,05', '1,95')
        self.assertContains(self.client.get('/admin/klienci/?q=anna@example.com'), 'Testowa')
        self.assertContains(self.client.get(self.wydanie()), '33,56 zł')
        self.client.post(self.wydanie())
        self.assertEqual(rezerwacje.rezerwacja(self.rezerwacja.id).stan, 'odebrana')
        sprzedaz, = magazyn.historia_sprzedazy(D, D)
        self.assertEqual((sprzedaz.rezerwacja_id, sprzedaz.suma), (self.rezerwacja.id, Decimal('33.56')))
        self.assertEqual((self.stan(self.ziemniaki), self.stan(self.marchew)), (Decimal('41.95'), Decimal('18.05')))

    def test_ta29_wydanie_nieprzygotowanej(self):
        przygotowanie = f'/admin/rezerwacje/{self.rezerwacja.id}/przygotuj/?dalej=wydaj'
        self.assertRedirects(self.client.get(self.wydanie()), przygotowanie)
        odpowiedz = self.przygotuj('8,05', '0', dalej='?dalej=wydaj')
        self.assertContains(odpowiedz, '25,76 zł')
        self.client.post(self.wydanie())
        self.assertEqual(rezerwacje.rezerwacja(self.rezerwacja.id).stan, 'odebrana')

    def test_ta30_klient_z_zaleglosci(self):
        self.zaleglosc(self.anna, '9.00', -2)
        self.przygotuj('8,05', '1,95')
        self.assertContains(self.client.get(self.wydanie()), 'Zaległość 9,00 zł')
        self.assertContains(self.client.get(f'/admin/klienci/{self.anna.pk}/'), 'Odnotuj wpłatę')
        self.client.post(self.wydanie())
        self.assertEqual(rezerwacje.rezerwacja(self.rezerwacja.id).stan, 'odebrana')


class PlanDostawyTests(Akceptacja):
    """PU26 Ustal plan dostawy. Plan ziemniaków na D+3: 100 kg, zarezerwowano 90 kg."""

    def setUp(self):
        super().setUp()
        self.zarezerwowano(self.ziemniaki, 3, 90)
        self.zaloguj(self.wlasciciel)

    def pole_planu(self, dni):
        return f'p{self.ziemniaki.id}-{self.dzien(dni).isoformat()}'

    def zapisz(self, dni, ilosc):
        dane = {
            f'p{w.produkt.id}-{k.dzien.isoformat()}': str(k.plan_kg)
            for w in rezerwacje.plan_tygodnia().wiersze for k in w.komorki if not k.zamkniety
        }
        return self.client.post('/admin/plan/', {**dane, self.pole_planu(dni): ilosc}, follow=True)

    def komorka(self, dane, dni):
        wiersz = next(w for w in dane.wiersze if w.produkt.id == self.ziemniaki.id)
        return next(k for k in wiersz.komorki if k.dzien == self.dzien(dni))

    def test_ta31_zmiana_planu(self):
        self.zapisz(3, '110')
        komorka = self.komorka(rezerwacje.plan_tygodnia(), 3)
        self.assertEqual((komorka.plan_kg, komorka.dostepne_kg), (Decimal(110), Decimal(20)))
        self.assertEqual(self.komorka(rezerwacje.katalog(), 3).dostepne_kg, Decimal(20))

    def test_ta32_plan_ponizej_zarezerwowanego(self):
        odpowiedz = self.zapisz(3, '80')
        self.assertIn('90', self.komunikaty(odpowiedz))
        self.assertEqual(self.komorka(rezerwacje.plan_tygodnia(), 3).plan_kg, Decimal(100))

    def test_ta33_dzien_zamkniety(self):
        self.ustaw_zegar(0, '18:00')
        self.assertNotContains(self.client.get('/admin/plan/'), f'name="{self.pole_planu(1)}"')
        self.zapisz(1, '50')
        self.assertEqual(self.komorka(rezerwacje.plan_tygodnia(), 1).plan_kg, Decimal(100))


class NiedostepnySerwerPoczty(BaseEmailBackend):
    def send_messages(self, wiadomosci):
        raise ConnectionRefusedError('serwer poczty niedostępny')


class OznaczNieodebraneTests(Akceptacja):
    """PU30 Oznacz nieodebrane rezerwacje. Na D: Anna 20 kg jabłek po 4,00 zł, Ola przygotowana, Ewa odebrana."""

    def setUp(self):
        super().setUp()
        self.jablka = self.produkt('Jabłka', '4.00')
        self.anna, self.ola, self.ewa = (self.klient(f'{imie}@example.com') for imie in ('anna', 'ola', 'ewa'))
        mail.outbox.clear()

    def rezerwacje_na_d(self):
        self.anna_r = self.zarezerwuj(self.anna, 0, (self.jablka, 20))
        self.ola_r = self.zarezerwuj(self.ola, 0, (self.ziemniaki, 5))
        self.ewa_r = self.zarezerwuj(self.ewa, 0, (self.ziemniaki, 3))
        self.dostawa(0, (self.jablka, 100), (self.ziemniaki, 100))
        rezerwacje.przygotuj_rezerwacje(self.ola_r.id, [(self.ziemniaki.id, Decimal(5))], self.sprzedawca)
        rezerwacje.przygotuj_rezerwacje(self.ewa_r.id, [(self.ziemniaki.id, Decimal(3))], self.sprzedawca)
        rezerwacje.wydaj_rezerwacje(self.ewa_r.id, self.sprzedawca)
        mail.outbox.clear()

    def o_18(self):
        with self.o_godzinie(0, '18:00'):
            call_command('oznacz_nieodebrane')

    def stan_rezerwacji(self, rezerwacja):
        return rezerwacje.rezerwacja(rezerwacja.id).stan

    def test_ta34_oplata_10_procent(self):
        self.rezerwacje_na_d()
        self.o_18()
        stany = [self.stan_rezerwacji(r) for r in (self.anna_r, self.ola_r, self.ewa_r)]
        self.assertEqual(stany, ['nieodebrana', 'nieodebrana', 'odebrana'])
        self.assertEqual(self.zaleglosc_klienta(self.anna), Decimal('8.00'))
        self.assertEqual(self.zaleglosc_klienta(self.ewa), 0)
        self.assertEqual(sorted(self.adresaci()), ['anna@example.com', 'ola@example.com'])

    def test_ta35_blokada_powyzej_100_zl(self):
        self.zaleglosc(self.anna, '95.00', -2)
        self.rezerwacje_na_d()
        self.o_18()
        dane = rozliczenia.zaleglosc_klienta(self.anna)
        self.assertEqual((dane.zaleglosc, dane.zablokowany), (Decimal('103.00'), True))
        wiadomosc, = [m for m in mail.outbox if m.to == ['anna@example.com']]
        self.assertIn('nie możesz składać nowych rezerwacji', wiadomosc.body)
        self.zaloguj(self.anna)
        self.assertContains(self.client.get(f'/rezerwacje/nowa/{self.dzien(2).isoformat()}/'), '103,00 zł')

    def test_ta36_brak_rezerwacji(self):
        self.o_18()
        self.assertEqual(mail.outbox, [])
        self.assertEqual(self.zaleglosc_klienta(self.anna), 0)

    def test_ta37_blad_poczty(self):
        self.rezerwacje_na_d()
        with self.settings(EMAIL_BACKEND='akceptacja.tests.NiedostepnySerwerPoczty'):
            self.o_18()
        self.assertEqual(self.stan_rezerwacji(self.anna_r), 'nieodebrana')
        self.assertEqual(self.zaleglosc_klienta(self.anna), Decimal('8.00'))
