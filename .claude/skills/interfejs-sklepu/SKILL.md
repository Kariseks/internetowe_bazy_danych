---
name: interfejs-sklepu
description: Projektowanie i weryfikacja polskiego i angielskiego interfejsu Warzywniaka w Django, w tym katalogu odbiorów i panelu personelu.
---

Gość wchodzi bezpośrednio do siedmiodniowego katalogu. Wybór dnia prowadzi do rezerwacji lub do logowania z powrotem do wybranego dnia. W tabeli zachowaj nazwę produktu, cenę za kilogram, jednostki i informację o zamkniętym terminie. Odbiór odbywa się w sklepie. Operacje personelu prowadź we własnych widokach panelu Django Admin. Podział ról i przebieg zakupu wynikają z `materialy/notatki/notatka_ze_spotkania_19_10_26.md`.

Projektuj formularze, zakładki i tabele od ich struktury HTML. Po wyłączeniu CSS użytkownik powinien odczytać kolejność, jednostki i etykiety pól. Stosuj jeden nagłówek główny, widoczny fokus i odnośnik pomijający nawigację. Sprawdź pełny proces samą klawiaturą, szerokość 320 px, zwykły i zwiększony kontrast. Stany dostępności opisuj słowem lub liczbą. Dla zwykłego tekstu przyjmij współczynnik kontrastu przynajmniej 4,5:1. [W3C WAI — struktura strony](https://www.w3.org/WAI/tutorials/page-structure/) i [WCAG 2.2 — kontrast](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html).

Teksty stałe w szablonach i Pythonie oznaczaj mechanizmami gettext Django. Kontrolki zmiany języka umieszczaj w obu panelach. Po przełączeniu zachowaj bieżącą stronę z parametrami zapytania, uprawnienia i walutę PLN. Przy zmianach sprawdź w PL i EN co najmniej treść, błędny formularz i potwierdzenie operacji. Zachowaj dane nadane przez użytkowników. [Django 5.2 — tłumaczenia](https://docs.djangoproject.com/en/5.2/topics/i18n/translation/).
