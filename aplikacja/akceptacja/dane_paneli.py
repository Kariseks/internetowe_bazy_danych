"""Powtarzalny stan początkowy testów widoków (identyfikatory używane w adresach testowych)."""
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.utils import timezone

from konta.models import ProfilKlienta
from magazyn.models import CenaProduktu, Dostawa, PozycjaDostawy, Produkt
from rezerwacje.models import PozycjaRezerwacji, Rezerwacja


class DanePaneli:
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        dzis = timezone.localdate()
        for pid, (nazwa, odmiana, cena) in enumerate([
            ('Ziemniaki', 'Irys', '3.20'), ('Marchew', '', '3.80'), ('Cebula', '', '3.50'),
            ('Pomidory', '', '14.90'), ('Ogórki', '', '8.90'), ('Kapusta', '', '3'),
            ('Buraki', '', '3.40'), ('Jabłka', '', '4.50'), ('Gruszki', '', '7.90'),
            ('Szparagi', '', '24'),
        ], start=1):
            p = Produkt.objects.create(pk=pid, nazwa=nazwa, odmiana=odmiana,
                                       standardowa_ilosc_kg=15 if pid == 9 else 100, w_ofercie=pid != 10)
            CenaProduktu.objects.create(produkt=p, cena_za_kg=cena, obowiazuje_od=dzis - timedelta(days=120))
        for uid, imie, nazwisko, login in [(11, 'Anna', 'Kowalska', 'kowalska'), (12, 'Piotr', 'Wiśniewski', 'wisniewski'),
                                           (13, 'Maria', 'Zielińska', 'zielinska'), (14, 'Tomasz', 'Lewandowski', 'lewandowski')]:
            email = login + '@example.com'
            user = User.objects.create(pk=uid, username=email, email=email, first_name=imie, last_name=nazwisko)
            ProfilKlienta.objects.create(uzytkownik=user, identyfikator_karty=f'tok_{uid}', telefon='500 000 000')
        for rid, uid, dni, stan, oplata in [
            (101, 11, 0, 'zlozona', None), (102, 12, 0, 'przygotowana', None), (103, 13, 0, 'zlozona', None),
            (201, 11, -1, 'odebrana', None), (202, 14, -2, 'nieodebrana', '118.60'), (203, 12, -2, 'nieodebrana', '12.40')
        ]:
            r = Rezerwacja.objects.create(pk=rid, klient_id=uid, dzien_odbioru=dzis + timedelta(days=dni), stan=stan,
                                          oplata_za_nieodebranie=oplata)
            for pid, masa in [(1, 10), (2, Decimal('3.5'))]:
                PozycjaRezerwacji.objects.create(rezerwacja=r, produkt_id=pid, ilosc_kg=masa,
                                                  masa_odwazona_kg=masa if stan in ('przygotowana', 'odebrana') else None)
        pracownik = User.objects.create_user('test-dostawy', is_staff=True)
        dostawa = Dostawa.objects.create(dzien=dzis - timedelta(days=1), zarejestrowal=pracownik)
        PozycjaDostawy.objects.create(dostawa=dostawa, produkt_id=1, ilosc_kg=5)


def historia_klienta(user):
    for rid, dni, stan in [(401, 2, 'zlozona'), (402, 0, 'przygotowana'), (403, -4, 'odebrana'),
                           (404, -8, 'nieodebrana'), (405, -11, 'anulowana')]:
        r = Rezerwacja.objects.create(pk=rid, klient_id=user.pk, dzien_odbioru=timezone.localdate() + timedelta(days=dni),
                                      stan=stan, oplata_za_nieodebranie=Decimal('12.40') if rid == 404 else None)
        PozycjaRezerwacji.objects.create(rezerwacja=r, produkt_id=1, ilosc_kg=10)
