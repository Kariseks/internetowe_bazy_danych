from django.core.management.base import BaseCommand
from django.utils import timezone

from rezerwacje import services


class Command(BaseCommand):
    help = 'PU30: uruchamiane przez cron o 18:00. Oznacza niewydane rezerwacje z bieżącego dnia i nalicza opłaty.'

    def handle(self, *args, **options):
        services.oznacz_nieodebrane(timezone.localdate())
