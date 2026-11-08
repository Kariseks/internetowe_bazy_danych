from django.core.management.base import BaseCommand
from django.utils import timezone

from rezerwacje import services


class Command(BaseCommand):
    help = 'PU31: uruchamiane przez cron o 6:00. Wysyła przypomnienia o odbiorze rezerwacji z bieżącego dnia.'

    def handle(self, *args, **options):
        wyslane, nieudane = services.wyslij_przypomnienia(timezone.localdate())
        self.stdout.write(f'Wysłano przypomnień: {wyslane}.')
        if nieudane:
            # Wyjście na stderr: cron przekaże je administratorowi.
            numery = ', '.join(str(r.id) for r in nieudane)
            self.stderr.write(f'Nie wysłano przypomnień o rezerwacjach: {numery}.')
