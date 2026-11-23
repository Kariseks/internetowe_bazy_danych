from django.db import models
from django.db.models import Case, F, Q, When
from django.utils import timezone


STANY_AKTYWNE = ("zlozona", "przygotowana")
STANY = (*STANY_AKTYWNE, "odebrana", "anulowana", "nieodebrana")


class Rezerwacja(models.Model):
    klient = models.ForeignKey("konta.ProfilKlienta", on_delete=models.PROTECT)
    dzien_odbioru = models.DateField()
    stan = models.CharField(max_length=12, default="zlozona")
    zlozono = models.DateTimeField(default=timezone.now)
    zmieniono = models.DateTimeField(auto_now=True)
    oplata_za_nieodebranie = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    aktywny_klient_id = models.GeneratedField(
        expression=Case(When(stan__in=STANY_AKTYWNE, then=F("klient_id"))),
        output_field=models.IntegerField(), db_persist=True, null=True,
    )

    class Meta:
        db_table = "rezerwacja"
        indexes = [models.Index(fields=["dzien_odbioru", "stan"], name="ix_rezerwacja_dzien_stan")]
        constraints = [
            models.UniqueConstraint(fields=["aktywny_klient_id", "dzien_odbioru"], name="uq_rezerwacja_aktywna"),
            models.CheckConstraint(condition=Q(stan__in=STANY), name="ck_rezerwacja_stan"),
            models.CheckConstraint(
                condition=(Q(stan="nieodebrana", oplata_za_nieodebranie__isnull=False, oplata_za_nieodebranie__gte=0)
                    | (~Q(stan="nieodebrana") & Q(oplata_za_nieodebranie__isnull=True))),
                name="ck_rezerwacja_oplata",
            ),
        ]


class PozycjaRezerwacji(models.Model):
    rezerwacja = models.ForeignKey(Rezerwacja, on_delete=models.CASCADE)
    produkt = models.ForeignKey("magazyn.Produkt", on_delete=models.PROTECT)
    ilosc_kg = models.DecimalField(max_digits=4, decimal_places=1)
    masa_odwazona_kg = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = "pozycja_rezerwacji"
        constraints = [
            models.UniqueConstraint(fields=["rezerwacja", "produkt"], name="uq_pozycja_rezerwacji"),
            models.CheckConstraint(condition=Q(ilosc_kg__gt=0, ilosc_kg__lte=20), name="ck_pr_ilosc"),
            models.CheckConstraint(condition=Q(masa_odwazona_kg__gte=0) | Q(masa_odwazona_kg__isnull=True),
                                   name="ck_pr_masa"),
        ]
