from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from magazyn.models import Produkt
from magazyn.services import dodaj_produkt


class Command(BaseCommand):
    help = 'Dodaje przykładowe produkty z cenami do pustego katalogu.'

    def add_arguments(self, parser):
        parser.add_argument('--dodaj-sztuki', action='store_true',
                            help='Uzupełnij istniejący katalog demonstracyjny o kalafior na sztuki.')

    def dodaj_kalafior(self):
        dodaj_produkt('Kalafior', '', 40, True, Decimal('6.50'), timezone.localdate(), 10, jednostka='szt')
        self.stdout.write('Dodano kalafior w cenie 6,50 zł/szt.')

    @transaction.atomic
    def handle(self, *args, **options):
        if Produkt.objects.exists():
            if options['dodaj_sztuki'] and not Produkt.objects.filter(nazwa='Kalafior', odmiana='').exists():
                self.dodaj_kalafior()
                return
            self.stdout.write('Katalog zawiera już produkty. Pominięto import.')
            return
        for nazwa, odmiana, plan, lada, cena in [
            ('Ziemniaki', 'Irys', 100, 60, '3.20'), ('Marchew', '', 60, 20, '3.80'),
            ('Cebula', 'żółta', 50, 15, '3.50'), ('Pomidory', 'malinowe', 30, 10, '14.90'),
            ('Ogórki', 'gruntowe', 30, 10, '8.90'), ('Buraki', '', 30, 10, '3.40'),
            ('Jabłka', 'Ligol', 80, 20, '4.50'), ('Gruszki', 'Konferencja', 25, 10, '7.90'),
        ]:
            dodaj_produkt(nazwa, odmiana, plan, True, Decimal(cena), timezone.localdate(), lada)
        self.dodaj_kalafior()
        self.stdout.write('Katalog demonstracyjny zawiera dziewięć produktów.')
