from django.conf import settings
from django.db import models
from django.db.models import F, Q
from django.utils import timezone


class Produkt(models.Model):
    nazwa = models.CharField(max_length=60)
    odmiana = models.CharField(max_length=60, blank=True, default="")
    standardowa_ilosc_kg = models.DecimalField(max_digits=7, decimal_places=2)
    ilosc_na_lade_kg = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    w_ofercie = models.BooleanField(default=True)

    class Meta:
        db_table = "produkt"
        constraints = [
            models.UniqueConstraint(fields=["nazwa", "odmiana"], name="uq_produkt_nazwa_odmiana"),
            models.CheckConstraint(condition=Q(ilosc_na_lade_kg__gte=0) &
                Q(standardowa_ilosc_kg__gte=F("ilosc_na_lade_kg")), name="ck_produkt_plan_lada"),
        ]

    def __str__(self):
        return f"{self.nazwa} ({self.odmiana})" if self.odmiana else self.nazwa


class CenaProduktu(models.Model):
    produkt = models.ForeignKey(Produkt, on_delete=models.PROTECT)
    cena_za_kg = models.DecimalField(max_digits=7, decimal_places=2)
    obowiazuje_od = models.DateField()

    class Meta:
        db_table = "cena_produktu"
        constraints = [
            models.UniqueConstraint(fields=["produkt", "obowiazuje_od"], name="uq_cena_produkt_od"),
            models.CheckConstraint(condition=Q(cena_za_kg__gt=0), name="ck_cena_dodatnia"),
        ]


class PlanDostawy(models.Model):
    produkt = models.ForeignKey(Produkt, on_delete=models.PROTECT)
    dzien = models.DateField()
    ilosc_kg = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        db_table = "plan_dostawy"
        constraints = [
            models.UniqueConstraint(fields=["produkt", "dzien"], name="uq_plan_produkt_dzien"),
            models.CheckConstraint(condition=Q(ilosc_kg__gte=0), name="ck_plan_ilosc"),
        ]


class Dostawa(models.Model):
    dzien = models.DateField(unique=True)
    zarejestrowano = models.DateTimeField(default=timezone.now)
    zarejestrowal = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    class Meta:
        db_table = "dostawa"


class PozycjaDostawy(models.Model):
    dostawa = models.ForeignKey(Dostawa, on_delete=models.CASCADE)
    produkt = models.ForeignKey(Produkt, on_delete=models.PROTECT)
    ilosc_kg = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        db_table = "pozycja_dostawy"
        constraints = [
            models.UniqueConstraint(fields=["dostawa", "produkt"], name="uq_pozycja_dostawy"),
            models.CheckConstraint(condition=Q(ilosc_kg__gte=0), name="ck_pd_ilosc"),
        ]


class Ubytek(models.Model):
    produkt = models.ForeignKey(Produkt, on_delete=models.PROTECT)
    masa_kg = models.DecimalField(max_digits=7, decimal_places=2)
    data_czas = models.DateTimeField(default=timezone.now, db_index=True)
    zarejestrowal = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    class Meta:
        db_table = "ubytek"
        constraints = [models.CheckConstraint(condition=Q(masa_kg__gt=0), name="ck_ubytek_masa")]


class KorektaStanu(models.Model):
    produkt = models.ForeignKey(Produkt, on_delete=models.PROTECT)
    roznica_kg = models.DecimalField(max_digits=7, decimal_places=2)
    przyczyna = models.CharField(max_length=200)
    data_czas = models.DateTimeField(default=timezone.now, db_index=True)
    zarejestrowal = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    class Meta:
        db_table = "korekta_stanu"
        constraints = [
            models.CheckConstraint(condition=~Q(roznica_kg=0), name="ck_korekta_roznica"),
            models.CheckConstraint(condition=~Q(przyczyna=""), name="ck_korekta_przyczyna"),
        ]


class Sprzedaz(models.Model):
    data_czas = models.DateTimeField(default=timezone.now, db_index=True)
    sprzedawca = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    rezerwacja = models.OneToOneField("rezerwacje.Rezerwacja", on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        db_table = "sprzedaz"


class PozycjaSprzedazy(models.Model):
    sprzedaz = models.ForeignKey(Sprzedaz, on_delete=models.CASCADE)
    produkt = models.ForeignKey(Produkt, on_delete=models.PROTECT)
    masa_kg = models.DecimalField(max_digits=6, decimal_places=2)
    cena_za_kg = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        db_table = "pozycja_sprzedazy"
        constraints = [
            models.UniqueConstraint(fields=["sprzedaz", "produkt"], name="uq_pozycja_sprzedazy"),
            models.CheckConstraint(condition=Q(masa_kg__gt=0), name="ck_ps_masa"),
            models.CheckConstraint(condition=Q(cena_za_kg__gt=0), name="ck_ps_cena"),
        ]
