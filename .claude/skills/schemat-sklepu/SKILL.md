---
name: schemat-sklepu
description: Aktualizuje modele Django, migracje i diagramy sklepu warzywnego, gdy zmieniają się reguły rezerwacji, dostaw, sprzedaży lub rozliczeń.
---

# Schemat sklepu

Odszukaj regułę dziedzinową w opisie przypadku użycia i porównaj ją z notatką ze spotkania. Rozdziel masę zamówioną od odważonej i cenę bieżącą od utrwalonej ceny sprzedaży. Stan magazynu wynika z ruchów towaru, a saldo z opłat i skutecznych rozliczeń. Wiersze pozycji łączą dokument i produkt. Dla każdej relacji sprawdź opcjonalność oraz unikalność obu końców.

Wprowadź zmianę w modelach, przygotuj migracje i uruchom je na osobnej bazie. Sprawdź na silniku docelowym reguły CHECK, klucze obce oraz unikalność aktywnej rezerwacji klienta na dzień. Reguły dotyczące sumy z wielu wierszy sprawdź przez serwis transakcyjny. [Migracje Django](https://docs.djangoproject.com/en/5.2/topics/migrations/) · [Ograniczenia modeli](https://docs.djangoproject.com/en/5.2/ref/models/constraints/)

Po migracji MySQL uruchom z katalogu `aplikacja` polecenie `python manage.py eksportuj_schemat`. Zapisuje DDL i pięć rysunków PDF do raportu. Sposób odtworzenia opisuje `baza/README.md`. Przy zmianie ograniczeń rezerwacji uruchom również `python manage.py test rezerwacje.test_schemat`. Zweryfikuj nazwy, typy, klucze i liczności. Wskaż silnik, zakres tabel dziedzinowych i mechanizm eksportu. Każdy fragment diagramu ma umożliwiać odczyt nazw i końców relacji przy normalnym powiększeniu PDF. Sprawdź oddzielnie tymczasową bazę SQLite i docelową MySQL, jeśli praca podaje wyniki dla obu. [MySQL SHOW CREATE TABLE](https://dev.mysql.com/doc/refman/8.4/en/show-create-table.html)
