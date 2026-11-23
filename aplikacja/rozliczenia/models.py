from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone


class RozliczenieZaleglosci(models.Model):
    klient = models.ForeignKey("konta.ProfilKlienta", on_delete=models.PROTECT)
    rodzaj = models.CharField(max_length=10)
    kwota = models.DecimalField(max_digits=8, decimal_places=2)
    skuteczne = models.BooleanField()
    data_czas = models.DateTimeField(default=timezone.now, db_index=True)
    zarejestrowal = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    class Meta:
        db_table = "rozliczenie_zaleglosci"
        constraints = [
            models.CheckConstraint(condition=Q(rodzaj__in=("wplata", "obciazenie")), name="ck_rozliczenie_rodzaj"),
            models.CheckConstraint(condition=Q(kwota__gt=0), name="ck_rozliczenie_kwota"),
            models.CheckConstraint(condition=Q(rodzaj="obciazenie") | Q(skuteczne=True), name="ck_rozliczenie_wplata"),
        ]
