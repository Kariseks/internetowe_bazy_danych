# Model bazy danych — `schema.sql`

`schema.sql` to model bazy danych z rozdziału „Model bazy danych” sprawozdania (słownik danych `tab:slownik`) zapisany jako DDL dla MySQL Community Server 8.4 LTS (InnoDB, `utf8mb4`, sortowanie `utf8mb4_pl_0900_ai_ci`). Służy do narysowania ERD (notacja Crow's Foot) w Visual Paradigm. Docelowo tabele tworzą migracje Django (`Meta.db_table` = nazwy z pliku), a tabele `auth_*` tworzy `django.contrib.auth`.

Skrypt tworzy osobną bazę `warzywniak_model` i na początku usuwa jej tabele, więc nie uruchamiać go na bazie aplikacji.

Gotowy diagram zapisać jako PNG w `dokumentacja/rysunki/diagramy/`:

- `erd-konceptualny.png` (encje, klucze i liczności, bez typów),
- `erd-logiczny.png` (tabele z atrybutami, typami, PK i FK).

Sprawozdanie wstawia te pliki samo (makro `\diagramvp`), gdy pojawią się w katalogu.

## 1. Załadowanie skryptu do MySQL

```bash
mysql -u root -p < baza/schema.sql
mysql -u root -p -e "SHOW TABLES FROM warzywniak_model;"   # 15 tabel
```

Skrypt sprawdzono tylko parserem SQL (dialekt MySQL). Na serwerze MySQL 8.4 nie był jeszcze uruchamiany.

## 2. Visual Paradigm Community Edition — ograniczenie

Na stronie porównania wydań (<https://www.visual-paradigm.com/editions/>) funkcje „Generate ERD from database” i „Generate & reverse DDL” w sekcji *Database engineering* nie są zaznaczone dla dwóch pierwszych kolumn. Prawdopodobnie są to wydania Community i Modeler; należy to sprawdzić w zainstalowanym programie. Community Edition pozwala rysować ERD (konceptualny, logiczny, fizyczny), ale prawdopodobnie **nie zaimportuje** `schema.sql` ani bazy automatycznie.

Możliwości:

**A. Ręczne narysowanie ERD w VP Community Edition (zalecane, spójne z pozostałymi diagramami)**

1. *Diagram → New → Entity Relationship Diagram*.
2. Dla każdej tabeli `CREATE TABLE` dodać encję (*Entity*) o tej samej nazwie. Kolumny dodać jako atrybuty z typem z pliku i zaznaczyć PK.
3. Związki rysować narzędziem *One-to-Many Relationship* (albo *One-to-One* dla `auth_user` – `profil_klienta` i `rezerwacja` – `sprzedaz`) od tabeli nadrzędnej do tabeli z kluczem obcym. VP dodaje kolumnę FK sam; wtedy usunąć duplikat albo przemianować ją na nazwę z pliku (np. `zarejestrowal_id`).
4. Liczności ustawić według tabeli `tab:zwiazki` w rozdziale 6.2 (np. *Rezerwacja – Pozycja rezerwacji*: 1 : 1..*).
5. Notacja: Crow's Foot to domyślna notacja ERD w VP. Sprawdzić w *Window → Project Options → Diagramming → Entity Relationship*.
6. Model konceptualny: kopia diagramu bez typów i bez tabeli `auth_user_groups` (związek *Konto – Rola* wiele do wielu).
7. Eksport: *Project → Export → Active Diagram as Image…*, format PNG, nazwa jak wyżej.

**B. Odtworzenie automatyczne w wydaniu z „Database engineering”** (np. Standard; wersja próbna albo licencja akademicka, jeśli uczelnia ją ma):

1. Załadować skrypt do MySQL (pkt 1).
2. *Tools → DB → Reverse Database…*, typ bazy *MySQL*, wskazać sterownik JDBC (VP proponuje pobranie MySQL Connector/J), host `localhost`, port `3306`, baza `warzywniak_model`, użytkownik i hasło.
3. Zaznaczyć wszystkie 15 tabel → *Finish*. VP tworzy ERD z tabelami i kluczami obcymi.
4. Ewentualnie *Tools → DB → Reverse DDL…* z plikiem `schema.sql`, bez serwera MySQL.
5. Sprawdzić liczności z `tab:zwiazki` i wyeksportować PNG jak w A.7.

**C. Kontrola poprawności narzędziem bezpłatnym:** MySQL Workbench (GPL), *Database → Reverse Engineer…* na bazie `warzywniak_model`, tworzy diagram EER w notacji Crow's Foot. Nadaje się do porównania z diagramem z VP. Do sprawozdania wstawiać diagram z VP, żeby wszystkie diagramy pochodziły z jednego narzędzia (3.3.1).

Nazwy poleceń menu podano według dokumentacji Visual Paradigm. W zainstalowanej wersji mogą się nieznacznie różnić.

## 3. Po implementacji

Po utworzeniu bazy przez migracje Django porównać ją z tym plikiem, np. `mysqldump --no-data` z bazy aplikacji i `diff` z `schema.sql`. Różnice opisać w rozdziale 7 i poprawić diagramy.
