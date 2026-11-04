# Indeks źródeł — sprawozdanie IBD (lokalny warzywniak)

Ścieżki względem repo `/home/karol-pc/Desktop/sem7/internetowe_bazy_danych/`. „s.” = numer strony pliku PDF (nie numer drukowany). Stan na 04.11.2026.

Hierarchia: **wytyczne v4 > notatka z konsultacji > decyzje Karola (PLAN.md) > przykłady**. Przykłady pokazują formę, nie fakty o warzywniaku.

---

## Część A. Źródła

### A1. Wytyczne i ustalenia projektu

**`materialy/IDB_wytyczne_v4.pdf`** — wytyczne prowadzącego IBD, wer. 4.0 (2021-10-04), 1 strona. **Źródło nadrzędne.**
- Zajęcia konsultacyjno-projektowe; grupy około 3-osobowe; temat „biznesowy” (z listy, własny lub temat pracy dyplomowej).
- Pkt 4 „Przygotowanie do realizacji”: (a) dobór grupy i podział obowiązków; (b) opis słowny w oparciu o SWOT (lub cele, problemy i CSF) + otoczenie podsystemu; (c) plan projektu na poziomie ogólnym; (d) cel, zakres, techniczna wykonalność i koszt wytworzenia; (e) harmonogram.
- Pkt 5 techniki modelowania: UML (zalecany, diagramy dobiera zespół), ERD/OZ + definicje obiektów, DHF/DNF, DFE lub inne. Projekt musi opisywać strukturę **funkcjonalną i informacyjną**.
- Pkt 6: prezentacja na forum grupy lub przed prowadzącym, razem z dokumentacją.
- Pkt 7–8: zalecane PHP lub Python + MySQL; dopuszczalne inne technologie.
- Pkt 9: architektura trójwarstwowa — kod oddzielony od statycznego HTML przez szablony (Smarty lub własne).
- Etapy: 1 przygotowanie, uzasadnienie i analiza problemu; 2 faza projektowa; 3 implementacja i walidacja; 4 wdrożenie; 5 prezentacja i zaliczenie.

**`materialy/notatki/notatka_ze_spotkania_19_10_26.md`** — notatka z konsultacji 19.10.2026 (prowadzący + 3-osobowy zespół).
- Sklep: mały, stacjonarny, warzywa i owoce.
- Cel biznesowy: ograniczenie strat z psucia się świeżego towaru dzięki wcześniejszej rezerwacji produktów przez klientów.
- Zakres: samo przeglądanie oferty to za mało; kluczowa jest rezerwacja konkretnych ilości (przykład: 100 kg ziemniaków) z odbiorem osobistym. Wykluczone: dowóz do domu, płatności online (płatność na miejscu).
- Technologia: Django (Python) + SQLite, aplikacja na fizycznym komputerze w sklepie, bez zewnętrznego hostingu.
- Przejrzano wstępny podział zadań, SWOT i harmonogram.
- Uwaga 1 (SQLite): prowadzący ostrzegł, że SQLite źle znosi jednoczesne zapisy wielu użytkowników. Zespół zaproponował kolejkowanie zapisów; temat do przemyślenia.
- Uwaga 2 (role): dotychczasowe role to właściciel, sprzedawca, dostawca i klient. Dodać „klienta-obserwatora”, który przegląda asortyment bez logowania i zakłada konto dopiero przy rezerwacji.
- Uwaga 3 (panele): panel Django Admin tylko dla sprzedawcy i właściciela; klienci dostają odrębny interfejs webowy (bezpieczeństwo, wygoda).
- Uwaga 4 (praca grupy): na analizie jeden student gra klienta/właściciela, dwóch prowadzi z nim wywiad jako analitycy. Projektowanie wspólnie (burza mózgów). Podział backend/frontend/BD dopiero przy implementacji.
- Uwaga 5 (SWOT): zbyt krótki czas (2 tygodnie na wdrożenie) to słaba strona, nie zagrożenie. Do zagrożeń dodać nieprzewidziane błędy techniczne przy kodowaniu. Wykreślić „brak kodu na etapie analizy” ze słabych stron.
- Uwaga 6 (formalne): wpisać konkretne wersje technologii (Django, Python); zaznaczyć licencje open source i uwzględnić w kosztorysie (0 zł za narzędzia). W podejściu code-first powstaje „model bazy danych” z klas ORM (reverse engineering), a nie klasyczny „projekt bazy”. W wdrożeniu: jasna instrukcja instalacji na komputerze stacjonarnym w sklepie.
- Ustalenia: 1 miesiąc na zamknięcie fazy projektowej (WF/WN, diagram PU, diagram klas ORM, poprawiony SWOT i kosztorys). Równolegle konfiguracja środowiska i prosta działająca wersja aplikacji. Zespół idzie zgodnie z harmonogramem.

**`PLAN.md`** (repo, working tree) — kolejka obowiązków i ustalenia.
- Grupa: Karol Gąsior 280913, Mikołaj Winiecki 280952, Mateusz Złośnik 281201; prowadzący dr inż. Roman Ptak.
- Terminy: 19.10 analiza, 17.11 projekt, 30.11 implementacja i wdrożenie, 14.12 prezentacja.
- Stack Django + SQLite, płatność poza systemem.
- Kolejka 1.1–5.6 z przypisaniem osób (zakres sprzed decyzji Q1 — bez rezerwacji). Status: 1.1 i 1.3–1.8 ✅, reszta ⬜.
- Styl: polski, forma bezosobowa, twarde spacje.

**`README.md`** — struktura repo, kompilacja `latexmk`, rysunki w `dokumentacja/figury/`, lista 5 etapów. Brak faktów o sklepie.

**`terminy.txt`** — w HEAD pusty plik, w working tree usunięty. Brak danych.

**`git show HEAD:dokumentacja/rozdzialy/01-analiza.tex`** — dawna treść etapu 1, sprzed konsultacji 19.10 i decyzji Q1. **Decyzja Q2: etap 1 pisze się od nowa; tej treści nie przywraca się i nie wkleja.** Poniższe fakty służą tylko jako lista tematów do potwierdzenia z Karolem w rozmowie o danej sekcji.
- § Grupa: kierunek Informatyka techniczna, W4N PWr; tabela składu; `longtable` obowiązków ogólnych i etapowych z osobą odpowiedzialną (jak w PLAN.md).
- § Opis słowny: jeden sklep, sprzedaż detaliczna przy ladzie; bez sprzedaży wysyłkowej, wielu punktów i kart lojalnościowych; płatność poza systemem. Produkty na wagę lub na sztuki, z nazwą, jednostką i aktualną ceną; asortyment sezonowy (dopisywanie, zmiana ceny, wycofanie). Dostawa: jeden dostawca, data przyjęcia, wiele pozycji (produkt + ilość) i zwiększenie stanu. Sprzedaż: zdarzenie z pozycjami po cenie z chwili sprzedaży, zmniejszenie stanu; nie można sprzedać więcej niż stan. Stan rośnie tylko przez dostawę, maleje tylko przez sprzedaż.
- § Problemy (1.2): pusty (`% TODO`).
- § Interesariusze: osoba prowadząca sklep i sprzedawca (użytkownicy, mogą być jedną osobą — rozdziela się role, nie etaty); dostawca i klient w otoczeniu, bez konta (**nieaktualne po Q1**). Brak integracji z kasą, sklepem internetowym i innym programem.
- § SWOT: S — 4 operacje, jasna reguła stanu, Django (formularze, admin, migracje), SQLite bez serwera. W — „brak kodu” (**do wykreślenia**), SQLite przy wielu zapisach, brak płatności. O — stany z ruchów zamiast pamięci i kartek, łatwa sezonowość. T — implementacja i wdrożenie w jednym terminie 30.11 (**przenieść do W**), rozrost zakresu, błąd przy zmianie ilości.
- § CSF: stan tylko z dostawy i sprzedaży, nieujemny; szybki zapis przy ladzie; wąski zakres; ścieżka produkt → dostawa → sprzedaż → stan na 14.12; kopia pliku bazy.
- § Cel i zakres: tabela „w zakresie / poza zakresem” (poza: wiele sklepów, płatności i kasa, lojalność, aplikacja mobilna, wysyłka, zamówienia do dostawcy).
- § Wykonalność: lokalne Django + SQLite, migracje, ORM, admin jako zapas; względny szacunek pracochłonności (tabela: analiza mniejszy, projekt średni, implementacja największy, wdrożenie i prezentacja mniejszy; bez godzin).
- § Harmonogram: tabela 05.10 (etap 0), 19.10, 17.11, 30.11 (3+4), 14.12.

**`dokumentacja/sprawozdanie.tex`** — strona tytułowa (kierunek Informatyka techniczna, przedmiot, tytuł, autorzy z indeksami, prowadzący, słowa kluczowe, WROCŁAW 2026), spis treści, Specyfikacja projektu i 14 rozdziałów na wzór „Sklepu hydraulicznego” z osobnymi nagłówkami dla wymogów wytycznych (04.11.2026); napisane 1.1–1.5. Kopie sprzed przebudów: `dokumentacja/sprawozdanie.pre-restructure.tex.bak`, `dokumentacja/sprawozdanie.pre-restructure2.tex.bak`.

**Środowisko deweloperskie (komputer Karola, odczyt 03.11.2026):** Ubuntu 24.04.5 LTS, Python 3.12.3, Django niezainstalowane. To **nie** jest komputer w sklepie.

### A2. Przykłady „Bazy danych” — `materialy/bazdy danych/`

Prowadzący przykładów: dr inż. Paweł Rogaliński (kurs BD, W12N). Wypożyczalnia rowerów to wzorcowy temat dokumentów etapowych.

**`Etapy realizacji projektu.pdf`** (1 s.) — 11 etapów: temat → opis świata rzeczywistego → cel → WF i WN → PU (aktorzy, diagram per aktor, scenariusze, makiety) → projekt BD (konceptualny ERD w notacji Chena → logiczny → fizyczny) → implementacja BD w SZBD → aplikacja realizująca PU → testy i wdrożenie → raport → prezentacja.

**`Opis świata rzeczywistego.pdf`** (2 s.) — wzór etapu 1 (wypożyczalnia rowerów). Nagłówek: nazwiska, grupa, data, „Etap: 1, Wersja: 1”. Proza: zasoby, role personelu i ich czynności, klienci i rejestracja, reguły biznesowe z liczbami. Sekcja „Parametry skalowalne” (początkowo/docelowo: stacje, rowery, użytkownicy, sezonowość, transakcje dziennie), formuły, cennik, liczba pracowników.

**`Wymagania funkcjonalne i niefunkcjonalne.pdf`** (4 s.) — wzór etapu 1 wer. 3: opis świata + WF (zakładanie kont, uwierzytelnianie z regułami hasła/PIN, funkcje per rola, „Uwaga: system nie prowadzi…”) + WN (SQL z darmową licencją komercyjną, serwer, terminale per rola, rodzaj UI) + „Funkcjonalności implementowane i testowane na zaliczenie”: wersja minimalna, standardowa, rozszerzona (s. 3–4).

**`Diagramy przypadków użycia - przykład dla wypożyczalni rowerów.pdf`** (6 s.) — etap 2: lista aktorów (gość, użytkownik, pracownik niezalogowany i zalogowany, role), rysunek aktorów, podział na moduły, diagram PU per moduł (s. 1–6, same rysunki).

**`Model Bazy danych.pdf`** (5 s.) — etap 3: (1) wstępny model pojęciowy: lista encji z opisem i grup relacji → uproszczony ERD; (2) model konceptualny (atrybuty identyfikacyjne i opisowe); (3) model logiczny z typami SZBD; normalizacja do 1NF, potem 2NF i 3NF — każdy krok z rysunkiem.

**`Opisy przypadków użycia oraz pr___interfejsu użytkownika - DEMO1.pdf`** (30 s.) — wycinek rozdz. 4 raportu „Sklep hydrauliczny” (te same treści, s. 21–50 raportu): scenariusze PU z makietami per aktor.

**`… - DEMO2.pdf`** (12 s.) — rozkład jazdy komunikacji: lista funkcji (s. 1), aktorzy gość/pasażer/administrator (s. 1), PU w modułach pasażera (8.1.1–8.1.9, s. 1–7) i administratora („PA”, 8.2.1–8.2.8, s. 8–12). Format: aktor, zdarzenie inicjujące, warunki początkowe, przebieg podstawowy, alternatywny, warunki końcowe, rysunek interfejsu.

**`… - DEMO3.pdf`** (16 s.) — kino: technologie (Spring Boot, Hibernate, Vaadin, Java 17), wersje min/std/rozsz. (1.6, s. 1), aktorzy i moduły Kino/Administracja/Kasa (1.7, s. 1–4), scenariusze PU z rysunkami (1.8, s. 5–16), zapowiedź modelu BD (1.9, s. 16).

**`Propozycje tematów projektów na rok akademicki 20242025.pdf`** (3 s.) — 13 tematów z listą funkcji (dziennik, restauracja, hotel, wypożyczalnie, kino, ranking…). Uwaga: temat własny po zatwierdzeniu. Warzywniaka brak; najbliższe analogie to rezerwacje (hotel, kino) i dostępność (wypożyczalnia narzędzi).

**`Restauracja - przykładowy raport.pdf`** (36 s.; Next.js, Supabase/PostgreSQL)
- Rozdz. 1 Opis świata + 1.1 parametry skalowalne + 1.2 liczba pracowników (s. 3).
- Rozdz. 2 aktorzy, moduły, diagramy PU per moduł (s. 4–6).
- Rozdz. 3 scenariusze w tabeli: aktor, cel, warunki wstępne, przebieg, wyjątki + zrzuty ekranów (s. 7–19).
- Rozdz. 4 encje, relacje słownie, ERD konceptualny i logiczny, 1–3NF w 3 punktach, tabela atrybutów (s. 19–21).
- Rozdz. 5: technologie z uzasadnieniem (5.1, s. 22), DDL `CREATE TABLE` (5.2, s. 22–23), link do repo (5.3), zmienione i niezrealizowane koncepcje (5.4, s. 23–24), problemy i rozwiązania z kodem (5.5, s. 24), omówienie fragmentu kodu (5.6, s. 25), ważne funkcjonalności (5.7, s. 26).
- Rozdz. 6 instrukcja obsługi: wymagania techniczne, start, role, zasady, instrukcja per rola ze zrzutami (s. 27–36).

**`Sklep hydrauliczny - przykładowy raport.pdf`** (102 s.; Spring Boot, Vaadin, MySQL, Docker) — najbliższa domena (sklep, asortyment, stan, zamówienia z odbiorem osobistym).
- Specyfikacja projektu: technologie, funkcje (s. 7–8).
- Rozdz. 1 Opis świata: role, dane osób, **stany zamówienia**, atrybuty produktu (jednostka, minimalny próg) (s. 9–10).
- Rozdz. 2: cel z „Uwagą” o wyłączeniach (2.1, s. 11); WF wg grup — konta, uwierzytelnianie, funkcje per rola, zalogowany, niezalogowany, proces zamówienia (2.2.1–2.2.8, s. 11–14); WN (2.3, s. 14); wersje min/std/rozsz. (2.4, s. 14).
- Rozdz. 3 aktorzy i diagramy PU dla modułów Administracja/Hurtownia/Sklep internetowy (s. 15–19).
- Rozdz. 4: poprawki diagramów względem poprzedniej wersji (4.1, s. 21); scenariusze PU z makietami (gość 4.2 s. 24–25, użytkownik 4.3 s. 26–33, pracownik 4.4 s. 35–45, kierownik 4.5 s. 46–50).
- Rozdz. 5: tabela postaci normalnych (s. 53–54); 6 wersji modelu z oceną NF (5.1–5.6, s. 54–65); **graf stanów zamówienia** z opisem stanów (5.7, s. 65–67).
- Rozdz. 6: technologie, warstwy, moduły, model danych, bezpieczeństwo (s. 69–70). Rozdz. 7: pakiety i klasy (s. 71–73). Rozdz. 8: kod z `@Transactional` (tworzenie zamówienia ze sprawdzeniem stanu s. 77–78, akceptacja, kompletowanie, odbiór, zwrot s. 78–85).
- Rozdz. 9 podręcznik: uruchomienie (build, Docker, baza, dostęp, s. 87–88); przewodnik per rola (s. 89–98).
- Rozdz. 10 wnioski: 5 numerowanych, konkretnych (czego nie zrobiono, co dalej, lekcja o iteracyjnym modelu danych) (s. 99). Spis rysunków (s. 100–102).

**`Szkółka narciarska - przykładowy raport.pdf`** (70 s.; Spring Boot, Vaadin, MySQL)
- Rozdz. 1 opis + parametry skalowalne (s. 5–6).
- Rozdz. 2: cel z „Uwagą” (s. 7); WF — konta, uwierzytelnianie (2FA symulowane), funkcje per rola z „Uwagami” (s. 7–10); WN (s. 10); wersje min/std/rozsz. (s. 10).
- Rozdz. 3 aktorzy, moduły, diagram PU per aktor + scenariusze (s. 11–40).
- Rozdz. 4: encje i relacje, uproszczony ERD, konceptualny, logiczny, normalizacja 1–3NF z uzasadnieniem (s. 41–43).
- Rozdz. 5 technologie i struktura (domena, repozytoria, serwisy, UI, bezpieczeństwo) (s. 45–47). Rozdz. 6 wybrana funkcjonalność z kodem (s. 49–52). Rozdz. 7 podręcznik per rola (s. 53–64).
- Rozdz. 8 wnioski (s. 65–66): m.in. „zrealizowano w pełni wersję standardową i częściowo rozszerzoną”. Rozdz. 9 uwagi o projekcie i zajęciach (s. 67).

### A3. Przykłady i instrukcje IO — `materialy/io/` (dr inż. Paweł Głuchowski, W4N)

**`Miniprojekt Biblioteka.pdf`** (68 s.) — kompletny przykład IO.
- Miejsce wdrożenia: nazwa projektu, klient, cel, zasoby ludzkie, przepisy i strategie (RODO, regulamin), dane techniczne (Ubuntu 24.04, jeden użytkownik naraz, lokalnie, limity danych) (s. 2).
- Wymagania F01–F08 i N01–N08 (s. 2–3).
- Diagram PU z analizą include/extend (s. 3–4).
- Słowny opis PU01–PU08: cel, warunki wstępne (z inicjatorem), warunki końcowe (z „Spełniono wymaganie Fxx”), scenariusz jako numerowany pseudokod (s. 4–11).
- Diagramy czynności (s. 11–13); diagram komponentów i klas Kontroler/Model (s. 14–19); kod (s. 19–26); diagramy sekwencji (s. 26–32); wynik działania (s. 32–35); kod klas (s. 35–58).
- Makiety okna + diagram stanów GUI (s. 59–60); testy jednostkowe (s. 61); akceptacyjne FitNesse (s. 62–64).

**`Modelowanie wymagań i przypadków użycia (L).pdf`** (6 s.) — Zad. 3: miejsce wdrożenia = zasoby ludzkie, przepisy i strategie, dane techniczne (s. 2). Zad. 4: numerowane WF/WN, niepodzielne (s. 2). Zad. 5: system, aktorzy, PU, uogólnienie, obowiązkowe przykłady «include» i «extend»; nazwy PU jak czynności (s. 3). Zad. 6: elementy opisu PU (s. 4). Ćwiczenia dekompozycji wymagań (s. 5–6).

**`Modelowanie realizacji przypadków użycia.pdf`** (5 s.) — diagram czynności dla 2 najbardziej złożonych PU: partycje = aktorzy, akcje jako czynności, obiekty, decyzja/merge, fork/join, obszar rozszerzenia (s. 1–3).

**`Modelowanie obiektowej 3-warstwowej architektury.pdf`** (7 s.) — diagram komponentów 3 warstw (prezentacja, kontrola, encje) połączonych interfejsami „lizak–łapka”; diagram klas warstwy kontroli i modelu; SOLID; wzorce fasada, metoda szablonowa lub strategia (s. 1–4).

**`Modelowanie interakcji między klasami i obiektami.pdf`** (5 s.) — diagramy sekwencji operacji realizujących PU, numerowane wiadomości, fragmenty loop/opt/alt, skrót kodu przy diagramie.

**`Modelowanie zmienności warstwy prezentacji.pdf`** (3 s.) — makiety (nazwa = przeznaczenie okna) + diagram stanów GUI (wyzwalacz [dozór] /akcja, entry/do/exit); lista typowych błędów (s. 2–3).

**`Testowanie jednostkowe operacji klas.pdf`** (4 s.) — testy w kolejności zależności, setUp/tearDown, ≥3 rodzaje asercji, ≥2 sposoby parametryzacji (JUnit; w Django odpowiednik: `TestCase` + `subTest`).

**`Testowanie akceptacyjne realizacji przypadków użycia.pdf`** (5 s.) — test całego systemu per PU: stan przed → operacja PU → stan po; jedna osoba = jeden PU (FitNesse; w Django odpowiednik: testy widoków z klientem testowym).

### A4. Szablony PWr — `materialy/formatki_pwr/`

- **`pd_inz_pl.doc`** — formatka strony tytułowej pracy inżynierskiej W4N: uczelnia, wydział, kierunek (3-literowy kod), specjalność, tytuł, dyplomant, opiekun, słowa kluczowe 3–6, WROCŁAW (rok).
- **`siw_pwr_2025-1.pdf`** (53 s.) — System Identyfikacji Wizualnej PWr (styczeń 2025): znak, ochrona znaku, zastosowania. Raport nie używa logo.
- **`szablon_pracy_dyplomowej_w_latex/`** — `main.tex` (strony tytułowe PL/EN przez `\includepdf`, abstrakt, wstęp, related work, rozdziały, zakończenie), `latex-settings.tex` (ustawienia, niebieskie linki), `bibliography.bib`, `chapters/*` (szablony treści), `title_page/pd_mgr_{pl,en}.pdf`, `images/LogoPWr.png`, PDF podglądowy. Źródło układu strony tytułowej (zasady w `.claude/skills/styl-sprawozdania/SKILL.md`).

---

## Część B. Podpunkt raportu → gdzie szukać

Numeracja wg szkieletu z 04.11.2026 (układ „Sklepu hydraulicznego” + osobne nagłówki dla każdego wymogu wytycznych v4 i notatki 19.10; `docs/plan-sprawozdania.md` §1, tam też „Wzorzec SH”). Fakty oznaczone H01 wolno użyć dopiero po potwierdzeniu przez Karola (Q2). Skróty: **W4** = wytyczne v4, **N19** = notatka 19.10, **H01** = `git HEAD:…/01-analiza.tex`, **SH** = Sklep hydrauliczny, **SZ** = Szkółka, **RE** = Restauracja, **BIB** = Miniprojekt Biblioteka, **ROW** = dokumenty wypożyczalni rowerów. ⛔ = brak faktów w źródłach (musi dostarczyć Karol); ◐ = częściowo. Kolumna „dawniej” podaje numer ze starego szkieletu etapowego.

### Specyfikacja projektu (bez numeru)

| Podpunkt | Fakty | Wzór formy | Status |
|---|---|---|---|
| Specyfikacja projektu | streszczenie rozdz. 1–2 i 8 (pisana na końcu; TODO w `.tex`) | SH s. 7–8 (cel, technologie i narzędzia, główne funkcje, uwagi) | ⛔ po napisaniu rozdz. 1–3 |

### Rozdz. 1. Opis słowny świata rzeczywistego (etap 1) — jak jest → dlaczego system → co zmienia

| Podpunkt | dawniej | Fakty | Wzór formy | Status |
|---|---|---|---|---|
| 1.1 Obecny sposób działania sklepu | 1.2 | N19 §1 (sklep, cel, rezerwacje, odbiór, płatność, bez dowozu) + uwaga 2 (role); H01 § Opis słowny (produkty, dostawy, sprzedaż, stan); (akapity „jak jest” dawnego opisu słownego) | ROW Opis świata s. 1–2; SH rozdz. 1 s. 9–10; BIB s. 2 | OK — Karol 04.11.2026 (Q7 w `CLAUDE.md`); **napisane**, uzupełnienia agenta do akceptacji |
| 1.2 Problemy bez systemu (P1–P8) | 1.3 | N19 §1 (straty z psucia się towaru); H01 § SWOT/O („pamięć albo kartki”) | W4 pkt 4b (problemy) | **napisane 04.11.2026** (P1–P3 i P5–P8 zatwierdzone przez Karola; P4, liczby i szczegóły opisu „jak jest” od agenta — do akceptacji; lista w `CLAUDE.md`) |
| 1.3 Proponowany system | 1.2 | Q7 w `CLAUDE.md` (rezerwacje, plan dostawy, opłata, karta, blokada, ewidencja, role); N19 §1 + uwaga 2 | SH rozdz. 1 (stany zamówienia, reguły dziedziny) s. 9–10; ROW Opis świata s. 1–2 | **napisane 04.11.2026** (akapity „po wprowadzeniu systemu” dawnego opisu słownego + zdanie przejścia), uzupełnienia agenta do akceptacji |
| 1.4 Interesariusze i otoczenie podsystemu | 1.4 | N19 uwagi 2–3 (role, panele); H01 § Interesariusze (do aktualizacji); decyzje Karola 04.11.2026: dostawca bez konta (dostawy wprowadza personel), operator płatności w otoczeniu systemu; decyzje Karola 04.11.2026 (1.4): zapłata za towar przy ladzie (gotówka, terminal) poza systemem, kasa fiskalna bez integracji | BIB „Zasoby ludzkie” s. 2 | **napisane 04.11.2026** (`tab:otoczenie`), uzupełnienia agenta do akceptacji (pkt 30–33 w `CLAUDE.md`) |
| 1.5 Parametry skalowalne | 1.2.1 | wartości przyjęte przez agenta na prośbę Karola (04.11.2026) | ROW s. 2; RE 1.1–1.2 s. 3; SZ 1.1 s. 6 | **napisane**, do akceptacji Karola |

### Rozdz. 2. Cel projektu oraz wymagania systemu (SH rozdz. 2; cel — etap 1, wymagania — etap 2)

| Podpunkt | dawniej | Fakty | Wzór formy | Status |
|---|---|---|---|---|
| 2.1 Cel projektu | 1.7 | N19 §1 (ograniczenie strat przez rezerwacje); P1–P8 (`sec:problemy`) | SH 2.1 s. 11; SZ 2.1 s. 7 | OK |
| 2.2 Zakres projektu | 1.7 | N19 §1 + uwagi 2–3; H01 § zakres (wyłączenia); decyzje 1.4 (zapłata za towar, kasa, terminal poza systemem) | SH 2.1 „Uwaga” s. 11 | OK (Q1) |
| 2.3 Wymagania funkcjonalne (2.3.1–2.3.8, kolejność SH) | 2.1 | N19 §1 (rezerwacja ilości, odbiór, płatność na miejscu) + uwagi 2–3; H01 opis (dostawy, sprzedaż, stan); Q7 w `CLAUDE.md` (reguły rezerwacji, opłata, blokada) | SH 2.2.1–2.2.8 s. 11–14; SZ 2.2.1 s. 7–10; BIB F01–F08 s. 2; IO Wymagania zad. 4 | ◐ — reguły haseł, uprawnienia właściciel vs sprzedawca ⛔ |
| 2.4 Wymagania niefunkcjonalne | 2.2 | N19 §1 (komputer w sklepie, bez hostingu, Django/SQLite) + uwaga 1 (współbieżność) + uwaga 3 (osobny panel); W4 pkt 7, 9 | SH 2.3 s. 14; SZ 2.2.2 s. 10; ROW Wymagania s. 3–4; BIB N01–N08 | ◐ — sprzęt, system, sieć, dostęp klientów ⛔ |
| 2.5 Wersje min/std/rozsz. | 1.7 | brak | SH 2.4 s. 14; SZ 2.3 s. 10; DEMO3 1.6; ROW Wymagania s. 4 | ⛔ podział |

### Rozdz. 3. Uzasadnienie potrzeby realizacji i organizacja projektu (etap 1; brak w SH — wymagania W4 4a–4e)

| Podpunkt | dawniej | Fakty | Wzór formy | Status |
|---|---|---|---|---|
| 3.1 Analiza SWOT | 1.5 | H01 § SWOT + N19 uwaga 5 (poprawki) | W4 pkt 4b | ◐ — akceptacja nowej wersji |
| 3.2 CSF | 1.6 | H01 § CSF (do uzupełnienia o rezerwacje) | W4 pkt 4b | ◐ |
| 3.3 Techniczna wykonalność systemu (3.3.1 wybór technologii, wersje i licencje; 3.3.2 współbieżne zapisy w SQLite) | 1.8 | N19 §1 (Django, SQLite, komputer w sklepie) + uwagi 1, 6; H01 § Wykonalność; A1 środowisko dev | — | ◐ — wersje (Q10); baza: SQLite (Q3 rozstrzygnięte 04.11.2026) |
| 3.4 Koszt wytworzenia systemu (kosztorys) | 1.7 | N19 uwaga 6 (0 zł narzędzia, licencje) | — | ◐ — praca (godziny, stawka), sprzęt ⛔ |
| 3.5 Plan projektu | 1.9 | PLAN.md kolejka; N19 „Ustalenia” (1 miesiąc na projekt, równoległa konfiguracja) | — | OK |
| 3.6 Grupa i podział obowiązków (3.6.1 skład grupy; 3.6.2 podział w etapach — N19 uwaga 4) | 1.1 | PLAN.md „Ustalenia”, kolejka; H01 § Grupa (tabele); N19 uwaga 4 (role w wywiadzie, wspólne projektowanie) | — | ◐ — kto grał właściciela w wywiadzie ⛔ |
| 3.7 Harmonogram | 1.10 | PLAN.md „Terminy”; H01 § Harmonogram (z 05.10) | — | OK |

### Rozdz. 4. Techniki modelowania (etap 2)

| Podpunkt | dawniej | Fakty | Wzór formy | Status |
|---|---|---|---|---|
| 4.1 Dobór technik modelowania i diagramów | — | W4 pkt 5 (UML zalecany; ERD/OZ + definicje obiektów; DHF/DNF; DFE) | IO instrukcje (dobór diagramów); Etapy realizacji (ROW) | ◐ — zestaw do decyzji (Q4) |
| 4.2 Struktura funkcjonalna i informacyjna | — | W4 pkt 5e | — | ◐ (Q4) |

### Rozdz. 5. Diagramy przypadków użycia (etap 2)

| Podpunkt | dawniej | Fakty | Wzór formy | Status |
|---|---|---|---|---|
| 5.1 Identyfikacja aktorów | 2.4 | N19 uwaga 2 (właściciel, sprzedawca, dostawca, klient, klient-obserwator); decyzja 04.11.2026: dostawca bez konta, więc nie jest aktorem systemu | ROW Diagramy PU s. 1; SH 3.1 s. 15; SZ 3.1 s. 11 | OK |
| 5.2 Diagramy PU per moduł | 2.4 | N19 (funkcje) | ROW s. 2–6; SH 3.2 s. 17–19; RE 2.2–2.5 s. 4–6; IO zad. 5 s. 3 | ◐ — lista PU do akceptacji |

### Rozdz. 6. Opis przypadków użycia (etap 2)

| Podpunkt | dawniej | Fakty | Wzór formy | Status |
|---|---|---|---|---|
| 6.1–6.4 Scenariusze PU + makiety (per rola) | 2.4 | brak gotowych | SH 4.2–4.5 s. 24–50 (= DEMO1); SZ 3.3 s. 15–40; DEMO2; DEMO3; RE 3 s. 7–19; BIB s. 4–11; IO zad. 6 s. 4; IO prezentacja zad. 1 | ⛔ przebiegi do akceptacji |
| 6.5 Diagramy czynności wybranych PU (+ ewentualnie stany GUI) | 2.5 | brak | IO realizacja PU s. 1–3; BIB s. 11–13; IO prezentacja zad. 2 | ⛔ (Q4) |

### Rozdz. 7. Model bazy danych (etap 2)

| Podpunkt | dawniej | Fakty | Wzór formy | Status |
|---|---|---|---|---|
| 7.1 Podejście code-first | — | N19 uwaga 6 (model z klas ORM, reverse engineering) | — | OK (forma) |
| 7.2 Identyfikacja encji i związków | 2.6 | H01 (produkt, dostawa, pozycje, sprzedaż, stan); N19 (rezerwacja, konta); Q7 (plan dostawy) | Model BD (ROW) s. 1–2; RE 4.1–4.2 s. 19–20; SZ 4.1 s. 41 | ◐ |
| 7.3 Model konceptualny (ERD) | 2.6 | jw. | Etapy realizacji (notacja Chena); Model BD s. 2–3; SZ 4.2 s. 42 | ◐ — notacja/narzędzie (Q5) |
| 7.4 Model logiczny i normalizacja | 2.6 | N19 uwaga 6 (code-first, z ORM) | Model BD s. 3–5; SZ 4.3–4.4 s. 43; RE s. 20; SH 5 tab. NF s. 53–54 | ◐ |
| 7.5 Diagram klas ORM | 2.6 | N19 uwaga 6 + „Ustalenia” | IO 3-warstwowa zad. 2; BIB s. 14–19 | ◐ — z kodu |
| 7.6 Słownik danych (definicje obiektów, W4 5b) | 2.6 | — | RE 4.3 tabela atrybutów s. 21 | ⛔ (z modeli) |
| 7.7 Graf stanów rezerwacji | 2.5 | N19 (rezerwacja → odbiór osobisty); Q7 (złożona → odebrana / anulowana / nieodebrana) | SH 5.7 s. 65–67; IO prezentacja zad. 2 | ◐ — reguły przejść do akceptacji |

### Rozdz. 8–11. Implementacja i walidacja (etap 3)

| Podpunkt | dawniej | Fakty | Wzór formy | Status |
|---|---|---|---|---|
| 8.1 Technologie | 3.1 | N19 §1 + uwaga 6; W4 pkt 7–8 | RE 5.1 s. 22; SH 6.1.1 s. 69; SZ 5.1 s. 45 | ◐ — wersje ⛔ |
| 8.2 Środowisko programistyczne i repozytorium kodu | — | N19 „Ustalenia” (konfiguracja środowiska, prosta działająca wersja); A1 środowisko dev | RE 5.3 (link do repozytorium) | ◐ — adres repozytorium ⛔ |
| 8.3 Architektura trójwarstwowa | 2.3 | W4 pkt 9 | IO 3-warstwowa zad. 1 s. 1–2; BIB s. 14; SH 6.1.2 s. 69 | OK (forma) |
| 8.4 Oddzielenie kodu od HTML – szablony Django | — | W4 pkt 9 | IO 3-warstwowa; SH 7.1.8 | ⛔ (z kodu) |
| 8.5 Moduły funkcjonalne | 3.2 | brak kodu | SH 6 s. 69–70; SZ 5.2 s. 45–47 | ⛔ (z repo, gdy powstanie) |
| 8.6 Panel klienta i panel administratora | 2.3 | N19 uwaga 3 | SH 6.1.2 s. 69 | OK (forma) |
| 8.7 Model fizyczny bazy danych | 3.3 | N19 uwaga 6 | RE 5.2 DDL s. 22–23 | ⛔ (z kodu) |
| 8.8 Bezpieczeństwo | — | N19 uwaga 3 | SH 6 s. 70; SZ 5.2 | ⛔ (z kodu) |
| 9.1 Aplikacje Django i modele | 3.3 | — | SH 7 s. 71–73 | ⛔ (z kodu) |
| 9.2 Widoki i szablony panelu klienta | 3.4 | N19 uwagi 2–3 | SH 7.1.8 s. 72; SZ 5.2 UI | ⛔ (z kodu, zrzuty) |
| 9.3 Konfiguracja panelu administratora | 3.5 | N19 uwaga 3 | — | ⛔ (z kodu) |
| 9.4 Pozostałe pliki | — | — | SH 7 s. 73 | ⛔ (z kodu) |
| 10 Fragment kodu | 3.6 | — | SH 8 s. 75–85; SZ 6 s. 49–52; RE 5.6 s. 25 | ⛔ |
| 11.1–11.2 Testy jednostkowe i akceptacyjne | 3.7 | — | IO testy jednostkowe; IO akceptacyjne; BIB s. 61–64 | ⛔ wyniki |
| 11.3 Zmiany i problemy | 3.8 | N19 uwaga 1 (temat SQLite otwarty) | RE 5.4–5.5 s. 23–24 | ⛔ |

### Rozdz. 12. Wdrożenie aplikacji i podręcznik dla użytkownika (etap 4)

| Podpunkt | dawniej | Fakty | Wzór formy | Status |
|---|---|---|---|---|
| 12.1.1 Środowisko uruchomieniowe w sklepie | 4.1 | N19 §1 (komputer w sklepie, bez hostingu) | SH 9.1 s. 87–88; RE 6.1 s. 27 | ⛔ sprzęt, system, sieć |
| 12.1.2 Instrukcja instalacji na komputerze w sklepie | 4.2 | N19 uwaga 6 (wymagana jasna instrukcja) | SH 9.1 s. 87–88 | ⛔ (po zbudowaniu) |
| 12.1.3 Dane początkowe i konta | 4.3 | — | — | ⛔ lista produktów, konta |
| 12.1.4 Kopia i odtwarzanie | 4.4 | H01 § CSF (kopia pliku bazy) | — | ◐ |
| 12.2 Przewodnik po rolach | 4.5 | — | RE 6 s. 27–36; SH 9.2 s. 89–98; SZ 7 s. 53–64 | ⛔ zrzuty |
| 12.3 Checklista odbioru | 4.6 | — | — | ⛔ wynik odbioru |
| 12.1.5 Dostęp do aplikacji | — | N19 §1 (komputer w sklepie) | SH 9.1.4 s. 88 | ⛔ adres, sieć (Q6) |

### Rozdz. 13–14. Prezentacja, zaliczenie i wnioski (etap 5)

| Podpunkt | dawniej | Fakty | Wzór formy | Status |
|---|---|---|---|---|
| 13.1 Plan prezentacji | 5.1 | W4 pkt 6; PLAN.md 5.1–5.5 | — | ⛔ podział wypowiedzi |
| 13.2 Materiały przekazywane do zaliczenia | — | W4 pkt 6 („wraz z dokumentacją”) | RE 5.3 | ⛔ |
| 14 Wnioski | 5.2 | — | SH 10 s. 99; SZ 8 s. 65–66; SZ 9 s. 67 | ⛔ ocena zespołu |

### Podpunkty bez źródła — co musi dostarczyć Karol

1. Kto w wywiadzie analitycznym grał właściciela, kto był analitykiem (3.6.2).
2. ~~Parametry skalowalne~~ — przyjęte przez agenta 04.11.2026, do akceptacji (1.5).
3. ~~Jak sklep działa dziś~~ — Karol 04.11.2026 (Q7), uzupełnienia agenta do akceptacji (1.1, 1.2, 1.3).
4. Podział funkcji na wersje minimalną, standardową i rozszerzoną (2.5).
5. Koszt pracy (godziny, stawka albo zgoda na szacunek względny); sprzęt w sklepie (3.4).
6. Wersje Pythona i Django (3.3.1, 8.1; Q10). Baza: SQLite (Q3 rozstrzygnięte 04.11.2026).
7. Reguły haseł; uprawnienia właściciela vs sprzedawcy (2.3). Reguły rezerwacji — Karol 04.11.2026 (Q7); dostawca bez konta — decyzja 04.11.2026.
8. Komputer w sklepie: system, sprzęt, sieć; jak klienci docierają do panelu (2.4, 12.1; Q6).
9. Akceptacja listy PU i ich przebiegów (5.2, 6).
10. Wszystko z rozdz. 8–14, co wynika z działającego kodu: struktura, modele, zrzuty, wyniki testów, zmiany i problemy, dane początkowe, wynik odbioru, wnioski, podział prezentacji.
