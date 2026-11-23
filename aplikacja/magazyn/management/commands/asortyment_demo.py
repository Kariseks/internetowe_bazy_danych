from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from magazyn.models import Produkt
from magazyn.services import dodaj_produkt


class Command(BaseCommand):
    help = 'Dodaje przykładowe produkty z cenami do pustego katalogu.'

    @transaction.atomic
    def handle(self, *args, **options):
        if Produkt.objects.exists():
            self.stdout.write('Katalog zawiera już produkty. Pominięto import.')
            return
        for nazwa, odmiana, plan, lada, cena in [
            ('Ziemniaki', 'Irys', 100, 60, '3.20'), ('Marchew', '', 60, 20, '3.80'),
            ('Cebula', 'żółta', 50, 15, '3.50'), ('Pomidory', 'malinowe', 30, 10, '14.90'),
            ('Ogórki', 'gruntowe', 30, 10, '8.90'), ('Buraki', '', 30, 10, '3.40'),
            ('Jabłka', 'Ligol', 80, 20, '4.50'), ('Gruszki', 'Konferencja', 25, 10, '7.90'),
        ]:
            dodaj_produkt(nazwa, odmiana, plan, True, Decimal(cena), timezone.localdate(), lada)
        self.stdout.write('Dodano osiem produktów z cenami i pulą na ladę.')
