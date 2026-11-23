# Handover: sprawozdanie IBD — lokalny warzywniak

Plik dla następnego agenta (Cursor / Claude Code). **Zakaz commitów i pushy.** Edycje tylko w lokalnym repo `/home/karol-pc/Desktop/sem7/internetowe_bazy_danych`. Karol commituje i pushuje sam.

Główny produkt: `dokumentacja/sprawozdanie.tex` (kompilacja: `cd dokumentacja && latexmk -g -pdf -interaction=nonstopmode sprawozdanie.tex`). Ostatni znany PDF: 66 stron, bez błędów.

Instrukcje: `CLAUDE.md` + `.claude/skills/styl-sprawozdania/SKILL.md` + `.claude/skills/zrodla-sprawozdania/SKILL.md`. Decyzje i lista „do akceptacji” są w `CLAUDE.md`.

---

## Co jest zrobione

### Sprawozdanie — napisane rozdziały

1. **Rozdz. 1** Opis słowny świata rzeczywistego — kompletny:
   - 1.1 Obecny sposób działania sklepu
   - 1.2 Problemy P1–P8
   - 1.3 Proponowany system (rezerwacje, plan dostawy, kaucja 10%, blokada >100 zł, ewidencja, role, atrybuty produktu, stany rezerwacji w tym „przygotowana do odbioru”)
   - 1.4 Interesariusze i otoczenie podsystemu (tabela; dostawca bez konta; operator płatności, kasa, terminal poza systemem; serwer poczty)
   - 1.5 Parametry skalowalne
2. **Rozdz. 2** Cel, zakres, WF1–WF48, WN, wersje min/std/rozsz. Rezerwacje są w wersji minimalnej. Reset hasła (min), maile (std), przypomnienie 6:00 (rozsz.).
3. **Rozdz. 3** SWOT, CSF, wykonalność (MySQL 8.4 LTS, Django 5.2, Python 3.12), kosztorys (zatwierdzony), plan, grupa (Prowadzi/Wspiera, zatwierdzone), harmonogram. Wdrożenie: mini PC + Ubuntu Server 24.04 + Nginx + Gunicorn + Let's Encrypt (Karol zatwierdził).
4. **Rozdz. 4** Aktorzy + lista PU1–PU31 (moduły: Konta, Rezerwacje, Magazyn i sprzedaż, Rozliczenia). Placeholdery diagramów VP.
5. **Rozdz. 5** 11+ scenariuszy PU (layout SH) + diagramy czynności (placeholdery). PU13 „Zarejestruj kartę płatniczą” (ponowne podpięcie / wymiana karty).
6. **Rozdz. 6** Model bazy: 15 tabel, związki, 3NF, słownik 74 atrybuty, graf stanów. Code-first Django, nazwy PL bez ogonków (`Meta.db_table`). Stan magazynu i zaległość **wyliczane**, nie przechowywane.

Rozdziały 7–13 (implementacja, klasy, fragment kodu, testy, wdrożenie/podręcznik, prezentacja, wnioski) oraz nienumerowana Specyfikacja projektu — **puste szkielety / TODO**.

### Inne pliki

- `baza/schema.sql` — DDL MySQL 8.4 InnoDB utf8mb4 (15 tabel). **Nie uruchomiony na prawdziwym MySQL** (na maszynie nie było serwera); sprawdzony parserem sqlglot.
- `baza/README.md` — jak narysować ERD w VP Community Edition (prawdopodobnie **nie ma** Reverse DDL/ERD z bazy).
- `dokumentacja/rysunki/diagramy/` i `dokumentacja/rysunki/ekrany/` — puste (`.gitkeep`). Placeholdery w `.tex` wstawiają PNG automatycznie, gdy plik pojawi się pod ustaloną nazwą (schemat w `CLAUDE.md` → „Rysunki — schemat nazw plików”). 11 diagramów + 14 ekranów.
- `docs/plan-sprawozdania.md`, `docs/indeks-zrodel.md` — aktualizowane razem ze szkieletem.

### Decyzje Karola (obowiązują)

- Temat: lokalny warzywniak (Jan Nowak, JDG, 6:00–18:00, asortyment PL na wagę, 1 dostawca 4:00).
- Rezerwacje w MVP: D+1…D+7, limit 20 kg, odbiór do 18:00, no-show = 10% z karty, blokada przy zaległości >100 zł. Plan dostawy = pula. Zamknięcie rezerwacji 18:00 dzień wcześniej.
- Dostawca bez konta. Płatność za towar i kasa fiskalna **poza** systemem. Operator płatności w otoczeniu (kaucja).
- Stack: **MySQL 8.4 LTS** (nie SQLite), Django 5.2 LTS, Python 3.12, `mysqlclient`. SQLite tylko do testów lokalnych.
- Klienci łączą się z serwerem Django; maksimum funkcji wbudowanych Django (auth, admin, forms, ORM, reset hasła, mail).
- Dane pracowników = pola User Django (login, imię, nazwisko, e-mail, hash hasła, grupa, active). Bez PESEL/adresu/telefonu. Klient loguje się e-mailem.
- Diagramy: **Visual Paradigm Community Edition**, notacja ERD **Crow's Foot** (jak w Sklepie hydraulicznym). Graf stanów rezerwacji zostaje.
- Makiety ekranów: placeholdery z nazwą pliku + „Zawartość ekranu” / odwołanie do scenariusza. Karol wrzuca PNG.
- Nie commituj.

Napięcia do potwierdzenia z prowadzącym (nie ruszać bez Karola): kaucja z karty vs „bez płatności online” w notatce 19.10; limit 20 kg vs przykład 100 kg ziemniaków.

---

## Na czym się wywalił agent

Agent `bc-1bb9cac6-678c-52bd-ac6a-b97cc8ed6e57` („Report skill and Claude handover”) na self-hosted workerze Karola (`6dfce98e-…`, katalog repo).

1. **Skończył** rozdz. 1–6, `baza/schema.sql`, placeholdery rysunków, poprawki (MySQL, Django, PU13 karta, podział obowiązków).
2. **Dostał zadanie** wygenerować `dokumentacja/schematy/`: 11 folderów, w każdym `.xmi` (UML 2 do importu w VP) + `.tex`/`.pdf` (TikZ jako wzór) + `README.md`, plus indeks i opcjonalnie `wszystkie.pdf`.
3. **Zaczął** (sprawdził tikz-uml — **brak** w TeX Live; strona edycji VP **nie wymienia XMI** dla Community; zebrał PU, encje, stany ze `sprawozdanie.tex` i `schema.sql`). **Nie zdążył zapisać** (albo zapisał bardzo mało) plików w `dokumentacja/schematy/`.
4. **Crash:** limit użycia modelu **Opus** na koncie Cursor: *You've hit your usage limit for Opus… reset 11/27/2026.* Tura zakończona `ERROR`. `SendToAgent` do tego agenta potem zwracał błąd.
5. Koordynator odpalił zastępcę `bc-59360a3e-b870-507b-bb8d-3577af2c25df` („Visual Paradigm diagram files”) na tym samym workerze, **bez** modelu Opus. Karol napisał **„czekaj stop”** — zastępca został zatrzymany (`aborted`) zanim skończył. **Nie wznawiać**, dopóki Karol nie każe.

Przed nową sesją: `ls dokumentacja/schematy/` — dokończ to, czego brakuje, nie nadpisuj bez potrzeby.

---

## Co jest do dokończenia

Kolejność sensowna (Karol: najpierw to, czego potrzeba **przed** rysowaniem w VP; implementację i testy później).

### A. Pliki diagramów (przerwane — to było bieżące zadanie)

Katalog `dokumentacja/schematy/<nazwa>/` dla:

| Folder | Diagram |
|---|---|
| `pu-aktorzy` | Aktorzy |
| `pu-modul-konta` | PU — Konta |
| `pu-modul-rezerwacje` | PU — Rezerwacje |
| `pu-modul-magazyn` | PU — Magazyn i sprzedaż |
| `pu-modul-rozliczenia` | PU — Rozliczenia |
| `czynnosci-pu08-zlozenie-rezerwacji` | Diagram czynności PU8 |
| `czynnosci-pu21-wydanie-rezerwacji` | Diagram czynności PU21 (uwaga: numery PU po dodaniu PU13) |
| `erd-konceptualny` | ERD konceptualny Crow's Foot |
| `erd-logiczny` | ERD logiczny |
| `klasy-modele-orm` | Klasy modeli Django |
| `stany-rezerwacja` | Graf stanów rezerwacji |

W każdym: `.xmi` (XML well-formed), `.tex` + skompilowany `.pdf` (plain TikZ, bez tikz-uml jeśli go nie ma), `README.md` (import VP, nazwa PNG do `dokumentacja/rysunki/diagramy/<nazwa>.png`). Na górze: `schematy/README.md`, ewent. `wszystkie.pdf`.

**Ograniczenia VP CE (sprawdzić w zainstalowanej kopii):**

- Reverse DDL / Generate ERD from database — prawdopodobnie **niedostępne** → rysować ERD ręcznie ze `schema.sql` albo PDF.
- Import XMI — **niepotwierdzony** na stronie edycji. Jeśli CE nie importuje XMI, Karol rysuje z PDF; XMI zostawić na próbę / edycję Standard.

Placeholderów w `sprawozdanie.tex` **nie ruszać** — Karol wstawia PNG z VP.

### B. Karol musi zrobić ręcznie w VP

Po A: import albo odrysowanie z PDF → eksport PNG do `dokumentacja/rysunki/diagramy/` (nazwy z `CLAUDE.md`). Ekrany analogicznie do `rysunki/ekrany/` (`puNN-<opis>.png`).

### C. Dalsze rozdziały sprawozdania (szkielety puste)

7 Opis implementacji → 8 Moduły i klasy → 9 Fragment kodu → 10 Testy → 11 Wdrożenie i podręcznik → 12 Prezentacja → 13 Wnioski → na końcu **Specyfikacja projektu**.

### D. Techniczne

- Odpal `baza/schema.sql` na MySQL 8.4 i popraw, jeśli padnie.
- Licencje: `mysqlclient` = GPL-2.0-or-later (już wpisane).
- Git: dużo `??` (`sprawozdanie.tex`, `CLAUDE.md`, `docs/`, `.claude/`, `baza/`, bak-i). Karol sam `git add` / commit / push. Bak-i (`sprawozdanie.pre-restructure*.tex.bak`) lepiej nie wrzucać.

### E. Otwarte do akceptacji Karola (nie blokują A)

Pełna lista w `CLAUDE.md`. Ważniejsze:

- Q11: polskie nazwy tabel + wyliczany stan/zaległość (pkt 80–81).
- Relacje «include»/«extend» PU (pkt 74).
- Szczegóły rozdz. 6 (pkt 80–86).
- Wymiana karty (oprócz ponownego podpięcia) — Karol powiedział „może podpiąć”; wymiana jest dopiskiem agenta.
- Dopiski etapu 1 (lista ~29+ pozycji, część już zatwierdzona w późniejszych odpowiedziach).
- Prowadzący: kaucja vs zakaz płatności online; 20 kg vs 100 kg.

Nie zaczynać od nowa rozdz. 1–6. Czytać `CLAUDE.md` przed każdą edycją `.tex`. Styl: `styl-sprawozdania` (zakaz fraz AI, twarde spacje).
