from django.db import connection
from django.test import TestCase
from django.urls import reverse


class SzkieletTests(TestCase):
    def test_katalog_dostepny_bez_logowania(self):
        odpowiedz = self.client.get(reverse('katalog'))
        self.assertEqual(odpowiedz.status_code, 200)
        self.assertTemplateUsed(odpowiedz, 'rezerwacje/katalog.html')

    def test_panel_administratora_wymaga_logowania(self):
        odpowiedz = self.client.get('/admin/')
        self.assertRedirects(odpowiedz, '/admin/login/?next=/admin/')

    def test_baza_to_mysql(self):
        self.assertEqual(connection.vendor, 'mysql')
