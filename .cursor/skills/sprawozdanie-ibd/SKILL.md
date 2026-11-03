---
name: sprawozdanie-ibd
description: Pisze i sprawdza sprawozdanie z projektu Internetowe bazy danych (lokalny warzywniak, Django + SQLite) zgodnie z materialy/IDB_wytyczne_v4.pdf. Użyj przy każdym obowiązku z PLAN.md, przy pytaniu o zgodność z wytycznymi i przed oddaniem etapu.
---

# Sprawozdanie IBD zgodne z wytycznymi v4

## Hierarchia źródeł

Przy sprzeczności wygrywa źródło wyżej na liście.

1. `materialy/IDB_wytyczne_v4.pdf` — instrukcja nadrzędna. Treść sprawozdania musi pokryć każdy punkt z tabeli „Wytyczne → miejsce w dokumentacji”.
2. Ostatnia jawna instrukcja użytkownika (o ile nie łamie wytycznych; jeśli łamie, wskaż konflikt i zapytaj).
3. `PLAN.md` — kolejka obowiązków, osoby, statusy, ustalenia.
4. `cursor.md`, `.cursor/rules/obowiazki.mdc`, `SKILL.md` — domena, stack, styl LaTeX, strona tytułowa.
5. Przykładowe projekty w `materialy/` (folder IO i folder baz danych) — wzór poziomu szczegółowości, rodzajów diagramów i układu tabel. Nie kopiuj z nich tekstu, domeny ani liczb.

## Wytyczne → miejsce w dokumentacji

| Punkt wytycznych | Wymóg | Miejsce | Obowiązki |
|------------------|-------|---------|-----------|
| 2, 4a | grupa ok. 3 osób, podział obowiązków | `01-analiza.tex`, Grupa projektowa | gotowe |
| 3 | temat „biznesowy” | `01-analiza.tex`, Opis słowny sklepu | 1.1 |
| 4b | opis słowny + SWOT (lub cele, problemy, CSF) + otoczenie podsystemu | `01-analiza.tex` | 1.1–1.5 |
| 4c | plan projektu na poziomie ogólnym | `01-analiza.tex`, Plan projektu i harmonogram | 1.10 |
| 4d | cel, zakres, wykonalność techniczna **i koszt wytworzenia** | `01-analiza.tex`, Cel systemu i zakres, Wykonalność | 1.6, 1.7, 1.9 |
| 4e | harmonogram | `01-analiza.tex`, Plan projektu i harmonogram | 1.8 |
| 5 | modelowanie struktury **funkcjonalnej i informacyjnej** | `02-projekt.tex`, Modelowanie, Projekt bazy danych | 2.4–2.9 |
| 7, 8 | technologia; inna niż zalecana (PHP/Python + MySQL) wymaga uzasadnienia | `02-projekt.tex`, Architektura systemu | 2.3 |
| 9 | architektura trójwarstwowa, kod oddzielony od HTML szablonami | `02-projekt.tex`, Architektura; `03-implementacja.tex` | 2.3, 3.1, 3.6, 3.7 |
| etap 3 | implementacja **i walidacja** | `03-implementacja.tex` | 3.1–3.9 |
| etap 4 | wdrożenie aplikacji | `04-wdrozenie.tex` | 4.1–4.6 |
| 6, etap 5 | prezentacja wraz z dokumentacją, zaliczenie | `05-ocena_efektow.tex` | 5.1–5.6 |

Numery obowiązków odpowiadają kolejce w `PLAN.md`.

## Reguły treści wynikające z wytycznych

- **Koszt wytworzenia (4d)** jest wymagany obok wykonalności. Rozbij go na pracę zespołu oraz koszty sprzętu, licencji i hostingu. Licencje Django, Pythona i SQLite są bezpłatne, co można stwierdzić bez danych od użytkownika. Godzin i stawek nie wymyślaj: bez danych zostaw `% TODO: godziny/stawka od grupy`.
- **Modelowanie (5)** ma opisać obie struktury. Informacyjna: ERD z definicjami encji (słownik danych), klucze, postać normalna. Funkcjonalna: diagram przypadków użycia oraz co najmniej jeden diagram zachowania (aktywności albo sekwencji) dla zapisu sprzedaży ze zmianą stanu. Same przypadki użycia i ERD to za mało.
- **Diagramy UML** dobiera się samodzielnie (5a). Przy każdym diagramie jedno zdanie, dlaczego wybrano ten rodzaj.
- **Trójwarstwowość (9)** opisz na Django: warstwa prezentacji to szablony HTML (`templates/`), warstwa logiki to widoki i formularze, warstwa danych to modele ORM i plik SQLite. Napisz wprost, że szablony Django pełnią rolę wskazanego w wytycznych Smarty. Panel administratora jest dodatkiem: ścieżka MVP musi mieć własne widoki z szablonami, inaczej nie widać oddzielenia kodu od HTML.
- **Technologia (7, 8)**: Python jest zalecany, SQLite nie. W architekturze uzasadnij SQLite (jedno stanowisko, brak serwera bazy, plik do kopii) i dodaj, że ORM pozwala przejść na MySQL zmianą `DATABASES` w ustawieniach.
- **Walidacja (etap 3)** to opis testu z wynikiem: przypadek, dane wejściowe, oczekiwany i uzyskany rezultat, w tabeli `booktabs`. Wyniki podaje użytkownik albo pochodzą z faktycznie uruchomionego testu.
- **Prezentacja (6)** odbywa się z dokumentacją; rozdział 5 zawiera scenariusz pokazu i wnioski, a PDF jest gotowy przed pokazem.

## Przykładowe projekty (IO, bazy danych)

Przy pierwszym użyciu po dodaniu folderów przejrzyj je i dopisz tu krótko:

- jakie diagramy zawierają i w którym rozdziale,
- jak zapisano słownik danych i wymagania (kolumny tabel),
- jak opisano testy i koszt.

Przenoś układ i poziom szczegółowości, nie treść. Jeśli przykład przeczy wytycznym v4, obowiązują wytyczne.

## Procedura dla jednego obowiązku

1. Odczytaj obowiązek z `PLAN.md` (numer, osoba, miejsce).
2. Znajdź w tabeli wyżej punkt wytycznych, który on realizuje, i sprawdź reguły treści dla tego punktu.
3. Przeczytaj sąsiednie podrozdziały, żeby nie powtarzać treści i zachować spójne nazwy (Produkt, Dostawa, PozycjaDostawy, Sprzedaż, PozycjaSprzedaży, StanMagazynowy — jedna konwencja).
4. Pisz we wskazaną `\subsection`. Styl z `SKILL.md`: polski, forma bezosobowa, twarde spacje (`w~`, `i~`, `z~`, `a~`, `o~`, `u~`), tabele `booktabs` z podpisem nad tabelą, każde `\label` ma odwołanie w tekście.
5. Rysunki: plik w `dokumentacja/figury/`, wstawiany przez `\figura{plik}{podpis}`. Bez pliku opisz rysunek słownie i zostaw `% TODO: rysunek`.
6. Bez danych od grupy (godziny, stawki, wyniki testów, czas próby) zostaw `% TODO` i wypisz braki w odpowiedzi.
7. Zaktualizuj `PLAN.md`: status ✅, linijka **Następny**, jedna linijka dziennika.

## Kontrola przed oddaniem etapu

- [ ] Każdy wiersz tabeli „Wytyczne → miejsce” dla tego etapu ma treść, a nie `% TODO`.
- [ ] Brak wymyślonych liczb; pozostałe `% TODO` są wypisane w odpowiedzi.
- [ ] Nazwy encji i modeli są takie same w tekście, diagramach i kodzie.
- [ ] Każda tabela i rysunek mają odwołanie w tekście.
- [ ] `latexmk -pdf main.tex` w `dokumentacja/` przechodzi bez błędów i bez niezdefiniowanych odwołań.
