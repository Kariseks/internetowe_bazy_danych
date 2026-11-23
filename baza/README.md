# Baza sklepu warzywnego

Schemat powstaje z modeli w aplikacjach `konta`, `magazyn`, `rezerwacje` i `rozliczenia`. Django tworzy tabele poleceniem `migrate`. Plik [schema.sql](schema.sql) jest eksportem definicji wszystkich tabel po migracjach na MySQL 8.4. Zawiera też tabele sesji, uprawnień i historii migracji.

## Odtworzenie DDL i diagramów

Uruchom MySQL zgodnie z [instrukcją aplikacji](../aplikacja/README.md), aktywuj środowisko Pythona i upewnij się, że polecenie `dot` (Graphviz) jest dostępne. Następnie z katalogu `aplikacja` wykonaj:

```bash
python manage.py migrate
python manage.py eksportuj_schemat
```

Polecenie czyta definicje przez `SHOW CREATE TABLE`. Sortuje je według zależności kluczy obcych i pomija bieżące wartości liczników. Tabele nie są modyfikowane. Aby zapisać wynik w osobnym katalogu, podaj `--katalog /ścieżka/do/eksportu`. Tryb SQLite umożliwia lokalne korzystanie z aplikacji. Eksport typów i ograniczeń do raportu korzysta z docelowego silnika MySQL.

Diagramy PDF w katalogu [dokumentacja/rysunki/diagramy](../dokumentacja/rysunki/diagramy) powstają na podstawie metadanych kolumn, indeksów unikalnych i kluczy obcych z `INFORMATION_SCHEMA`:

| Rysunek | Zakres |
| --- | --- |
| `erd-konceptualny.pdf` | Powiązania encji i przypisanie ról |
| `erd-asortyment.pdf` | Produkty, historia cen i plany dostaw |
| `erd-magazyn.pdf` | Przyjęcia, pozycje dostaw, ubytki i korekty |
| `erd-rezerwacje.pdf` | Rezerwacje, sprzedaże i ich pozycje |
| `erd-rozliczenia.pdf` | Konta, grupy, profile klientów i rozliczenia |

Zielony nagłówek oznacza tabelę rozpisaną w danym obszarze. Szary nagłówek identyfikuje tabelę z innego obszaru, w którym znajduje się jej pełny opis. PK oznacza klucz główny, FK klucz obcy, UQ unikalność, ƒ kolumnę generowaną, a znak zapytania przy typie dopuszczalną wartość NULL. Kółko na końcu linii oznacza dolną granicę równą zero, kreska jedną instancję, a rozgałęzienie wiele instancji. Liczności wynikają z ograniczeń bazy. Serwis może wymagać co najmniej jednej pozycji, gdy zapisuje cały dokument w transakcji.

## Kontrola eksportu

Wybierz osobną, pustą bazę testową. Poniższe polecenia wczytują tylko definicje i wypisują odtworzone tabele:

```bash
mysql -u użytkownik -p nazwa_pustej_bazy < baza/schema.sql
mysql -u użytkownik -p nazwa_pustej_bazy -e "SHOW TABLES"
```

Do instalacji aplikacji użyj migracji. Eksport DDL służy do inspekcji i odtworzenia struktury, a wpisy historii wykonanych migracji są danymi aplikacji.
