from django.conf import settings
from django.db import models
from django.utils import timezone


class ProfilKlienta(models.Model):
    uzytkownik = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, primary_key=True)
    telefon = models.CharField(max_length=20, db_index=True)
    jezyk = models.CharField(max_length=2, choices=[("pl", "Polski"), ("en", "English")], default="pl")
    identyfikator_karty = models.CharField(max_length=64, null=True, blank=True, unique=True)
    regulamin_zaakceptowano = models.DateTimeField(default=timezone.now)
    zanonimizowano = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "profil_klienta"
        constraints = [
            models.CheckConstraint(condition=models.Q(jezyk__in=("pl", "en")), name="ck_profil_jezyk"),
        ]
