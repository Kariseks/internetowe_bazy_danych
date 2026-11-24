from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.test import TestCase

from konta.models import ProfilKlienta
from magazyn.models import Produkt
from .models import PozycjaRezerwacji, Rezerwacja


class OgraniczeniaSchematTests(TestCase):
    """Weryfikacja ograniczeń SQL przy zapisie z pominięciem formularzy i serwisów."""

    @classmethod
    def setUpTestData(cls):
        cls.profil = ProfilKlienta.objects.create(uzytkownik=User.objects.create(username="klient"))
        cls.produkt = Produkt.objects.create(nazwa="Seler", standardowa_ilosc_kg=30)
        cls.rezerwacja = Rezerwacja.objects.create(klient=cls.profil, dzien_odbioru=date(2026, 11, 27))

    def test_tylko_jedna_aktywna_rezerwacja_klienta_na_dzien(self):
        parametry = dict(klient=self.profil, dzien_odbioru=self.rezerwacja.dzien_odbioru)
        with self.assertRaises(IntegrityError), transaction.atomic():
            Rezerwacja.objects.create(**parametry, stan="przygotowana")
        Rezerwacja.objects.filter(pk=self.rezerwacja.pk).update(stan="anulowana")
        kolejna = Rezerwacja.objects.create(**parametry)
        kolejna.refresh_from_db()
        self.assertEqual(kolejna.aktywny_klient_id, self.profil.pk)
        self.rezerwacja.refresh_from_db()
        self.assertIsNone(self.rezerwacja.aktywny_klient_id)

    def test_oplata_tylko_dla_nieodebranej(self):
        rekord = Rezerwacja.objects.filter(pk=self.rezerwacja.pk)
        for stan, kwota in [("nieodebrana", None), ("odebrana", Decimal("2.00")), ("nieodebrana", Decimal("-1.00"))]:
            with self.subTest(stan=stan, kwota=kwota), self.assertRaises(IntegrityError), transaction.atomic():
                rekord.update(stan=stan, oplata_za_nieodebranie=kwota)
        rekord.update(stan="nieodebrana", oplata_za_nieodebranie=Decimal("2.00"))

    def test_unikat_produktu_i_masa_pozycji(self):
        dokument = dict(rezerwacja=self.rezerwacja, produkt=self.produkt)
        with self.assertRaises(IntegrityError), transaction.atomic():
            PozycjaRezerwacji.objects.create(**dokument, ilosc_kg=0)
        PozycjaRezerwacji.objects.create(**dokument, ilosc_kg=1)
        with self.assertRaises(IntegrityError), transaction.atomic():
            PozycjaRezerwacji.objects.create(**dokument, ilosc_kg=2)
