---
name: transakcje-sklepu
description: Prowadzi implementację i weryfikację trwałego zapisu rezerwacji, sprzedaży i rozliczeń w projekcie sklepu.
---

# Zapis w sklepie

Punktem odniesienia są scenariusze PU w sprawozdaniu i testy akceptacja/tests.py. Utrzymaj publiczne nazwy usług wykorzystywane w obu panelach.

* Przy rezerwacji blokuj profil i produkty w ustalonej kolejności. Po otrzymaniu blokad sprawdź termin w Europe/Warsaw, limit 20 kg i pulę produktu po odjęciu ilości na ladę i rezerwacji. Przy zmianie pomiń własne dotychczasowe pozycje.
* Wydanie łączy zapis sprzedaży, cen i mas po zważeniu ze zmianą stanu rezerwacji w jednej transakcji. Przy sprzedaży przy ladzie uwzględnij dzisiejsze niewydane rezerwacje. Historyczne obroty odczytuj po utrwalonej cenie sprzedaży.
* Przy ponownym oznaczeniu nieodebranych wybieraj tylko rezerwacje otwarte. Opłata zależy od zarezerwowanej masy oraz ceny w dniu odbioru. Weryfikuj granicę blokady konta przy dokładnie 100 zł i po jej przekroczeniu.
* Sprawdź wyścig dwóch klientów o ostatnią dostępną ilość na silniku z blokadami wierszy. Uruchom ponownie migracje oraz testy przed wpisaniem wyników do raportu.

Źródła techniczne: [transakcje Django](https://docs.djangoproject.com/en/5.2/topics/db/transactions/) i [blokady wierszy](https://docs.djangoproject.com/en/5.2/ref/models/querysets/#select-for-update).
