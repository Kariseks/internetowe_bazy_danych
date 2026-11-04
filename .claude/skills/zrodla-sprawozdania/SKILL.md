---
name: zrodla-sprawozdania
description: Skąd brać fakty i formę do sprawozdania IBD (lokalny warzywniak) oraz jakie elementy musi mieć każdy z 5 etapów wg wytycznych v4. Użyj przed omówieniem z Karolem lub napisaniem dowolnej sekcji dokumentacja/sprawozdanie.tex oraz przy sprawdzaniu kompletności sekcji.
---

# Źródła i wymagane elementy sprawozdania IBD

## Hierarchia źródeł

1. `materialy/IDB_wytyczne_v4.pdf` — **nadrzędne**. Pięć etapów (przygotowanie i~analiza, faza projektowa, implementacja i~walidacja, wdrożenie, prezentacja i~zaliczenie); pkt 4a–e (grupa i~obowiązki; opis słowny + SWOT lub cele/problemy/CSF + otoczenie; plan ogólny; cel/zakres/wykonalność/koszt; harmonogram); pkt 5 (techniki modelowania — struktura **funkcjonalna i~informacyjna**); pkt 9 (architektura trójwarstwowa, kod oddzielony od HTML przez szablony).
2. Ustalenia z~konsultacji: `materialy/notatki/*.md` (19.10.2026: rezerwacje klientów, klient-obserwator, osobny panel klienta, ostrzeżenie o~SQLite, wersje technologii, licencje i~0~zł za narzędzia, „model bazy danych” z~klas ORM, instrukcja instalacji w~sklepie).
3. Decyzje Karola: dziennik decyzji w `CLAUDE.md` i §5 w `docs/plan-sprawozdania.md`.
4. Przykłady: `materialy/bazdy danych/` (raporty Restauracja, Sklep hydrauliczny, Szkółka narciarska; dokumenty etapowe wypożyczalni rowerów; DEMO1–3) i~`materialy/io/` (Miniprojekt Biblioteka + instrukcje IO). Dają formę, głębokość i~dobór diagramów, **nie fakty o~warzywniaku**. Przy sprzeczności z~wytycznymi v4 wygrywają wytyczne.

## Gdzie szukać informacji

Przed omówieniem lub napisaniem **każdego** podpunktu otwórz `docs/indeks-zrodel.md`:

- Część A: każde źródło z~listą faktów i~numerami stron PDF.
- Część B: dla każdego podpunktu raportu plik i~miejsce z~faktami oraz osobno wzór formy, ze statusem OK / ◐ / ⛔.
- ⛔ = brak źródła → pytasz Karola, nie piszesz.

Plan całości (wzorzec SH, szkielet i~tabela pokrycia wytycznych, pytania Q1–Q14, plan aplikacji, kolejność omawiania etapu 1): `docs/plan-sprawozdania.md`.

Skrót najczęstszych miejsc:

| Podpunkt | Fakty | Wzór formy |
|---|---|---|
| Opis, cel, zakres, role | `materialy/notatki/notatka_ze_spotkania_19_10_26.md`; reszta od Karola | Sklep hydrauliczny rozdz. 1–2 |
| SWOT, CSF, wykonalność, koszt | notatka (uwagi 1, 5, 6); reszta od Karola | wytyczne v4 pkt 4 |
| Wymagania, aktorzy, PU, scenariusze | notatka; reguły ⛔ | Sklep hydrauliczny rozdz. 2–4, Szkółka rozdz. 2–3, Biblioteka s. 2–11 |
| Model bazy danych | notatka (code-first), kod | `Model Bazy danych.pdf`, Szkółka rozdz. 4, Sklep hydrauliczny rozdz. 5 |
| Implementacja, wdrożenie, podręcznik | kod i~wyniki uruchomień; komputer w~sklepie ⛔ | Restauracja rozdz. 5–6, Sklep hydrauliczny rozdz. 6–9 |
| Wnioski | ocena zespołu ⛔ | Sklep hydrauliczny rozdz. 10 |

Dawna treść etapu 1 w~git (`git show HEAD:dokumentacja/rozdzialy/01-analiza.tex`) jest sprzed decyzji o~rezerwacjach i~**nie jest źródłem tekstu** (decyzja Q2). Fakty z~niej ([H01] w~`docs/`) to tylko tematy do potwierdzenia z~Karolem.

PDF-y czyta się bezpośrednio (narzędzie odczytu plików) albo przez `pdftotext -layout "<plik>.pdf" -` (poppler-utils), jeśli jest zainstalowany.

## Struktura raportu (wzór: Sklep hydrauliczny)

Raport ma układ i~logikę wywodu raportu „Sklep hydrauliczny” (SH; pełny spis rozdziałów SH z~zawartością: `docs/plan-sprawozdania.md` §1 „Wzorzec SH”), uzupełnione o~elementy wytycznych v4, których SH nie ma. Kolejność myśli:

1. **Jak jest** (1.1) — sklep dziś, bez systemu: kto, co robi, jak płyną towar, informacja i~pieniądze. Czas teraźniejszy, zero funkcji systemu.
2. **Dlaczego system** (1.2) — problemy P1–P8 wynikające z~opisu „jak jest”: problem, skutek z~liczbą, mechanizm systemu, który go rozwiązuje (krótko, z~odwołaniem do 1.3).
3. **Co system wprowadza i~zmienia** (1.3) — reguły pracy po wdrożeniu (rezerwacje, plan dostawy, opłata, ewidencja) i~role; w~SH to część rozdz. 1 (stany zamówienia, atrybuty produktu). Potem otoczenie (1.4) i~parametry skalowalne (1.5).
4. **Cel i~wymagania** (rozdz. 2, jak SH 2) — osobno cel i~zakres z~„Uwagą”, WF w~kolejności SH, WN, wersje.
5. **Uzasadnienie potrzeby realizacji i~organizacja** (rozdz. 3, z~wytycznych, brak w~SH) — SWOT, CSF, techniczna wykonalność (wybór technologii, techniki modelowania i~narzędzie Visual Paradigm, współbieżność w~MySQL), kosztorys, plan, grupa (skład, podział w~etapach), harmonogram.
6. Dalej jak SH: diagramy PU (4, wstęp = struktura funkcjonalna) → opis PU (5, z~diagramami czynności) → model bazy danych (6, wstęp = struktura informacyjna; od podejścia code-first) → implementacja (7: technologie, środowisko i~repozytorium, architektura trójwarstwowa, szablony, moduły, panele, model fizyczny, bezpieczeństwo) → moduły i~klasy (8) → fragment kodu (9); potem walidacja i~testy (10), wdrożenie aplikacji i~podręcznik (11), prezentacja i~zaliczenie (12), wnioski (13). Osobnego rozdziału „Techniki modelowania” nie ma (decyzja Karola 04.11.2026): techniki (UML: przypadki użycia, czynności, klasy; ERD) i~narzędzie Visual Paradigm opisuje 3.3.1.

Zasada nazewnictwa: każdy element wytycznych v4 i~notatki 19.10 ma własny nagłówek o~nazwie bliskiej brzmieniu wytycznych (np. „Techniczna wykonalność systemu”, „Otoczenie podsystemu”, „Słownik danych (definicje obiektów)”), żeby prowadzący znalazł go w~spisie treści. Mapa wymóg → sekcja: `docs/plan-sprawozdania.md` §1 „Pokrycie wymagań”.

Etapy wytycznych → rozdziały: etap 1 → 1, 2.1–2.2, 3; etap 2 → 2.3–2.5, 4–6; etap 3 → 7–10; etap 4 → 11; etap 5 → 12–13. Nienumerowaną „Specyfikację projektu” (SH s. 7–8) pisze się na końcu.

## Wymagane elementy — etap 1: Przygotowanie i~uzasadnienie (rozdz. 1–3)

Kolejność omawiania z~Karolem: `docs/plan-sprawozdania.md` §7.

| Element (sekcja) | Forma | Uwagi z~przykładów / konsultacji |
|---|---|---|
| Obecny sposób działania sklepu (1.1) | 4–6 akapitów prozy | Jak jest dziś: działalność, asortyment, personel, dostawy, sprzedaż przy ladzie. Bez funkcji systemu (wzór: SH rozdz. 1, ROW „Opis świata”). |
| Problemy bez systemu (1.2) | numerowana lista P1–P8 + akapit | Problem → skutek z~liczbą → mechanizm systemu. Numeracja i~etykiety `prob:` stałe. |
| Proponowany system (1.3) | proza + lista ról (`description`) | Reguły pracy po wdrożeniu i~to, co się zmienia; role (notatka uwaga 2: klient-obserwator). |
| Interesariusze i~otoczenie podsystemu (1.4) | tabela: interesariusz, relacja, oczekiwanie | Granica systemu: co w~systemie, co poza nim (dostawca bez konta, operator płatności, płatność za towar, dowóz). |
| Parametry skalowalne (1.5) | tabela „początkowo / docelowo” + akapit spójności | Wzór ROW s. 2, RE 1.1. |
| Cel projektu (2.1) | proza | Wzór SH 2.1; odwołania do P1–P8. |
| Zakres projektu (2.2) | proza + tabela „w~zakresie / poza” + „Uwaga:” | Zakres wg Q1 i~decyzji z~1.4. Wersje minimalna / standardowa / rozszerzona w~2.5 (wzór: SH 2.4, Szkółka 2.3). |
| SWOT (3.1) | tabela 4 pola | Słabe = wewnętrzne (np. 2~tygodnie na wdrożenie); zagrożenia = zewnętrzne (np. nieprzewidziane błędy techniczne). Bez „brak kodu na etapie analizy”. |
| CSF (3.2) | tabela: czynnik, skutek braku | Sprawdzalne na działającej aplikacji. |
| Techniczna wykonalność systemu (3.3) | proza; 3.3.1 wybór technologii, wersje i~licencje; 3.3.2 współbieżne zapisy w~MySQL (InnoDB) | Stos z~**konkretnymi wersjami** (Python 3.12, Django 5.2 LTS, MySQL 8.4 LTS) i~technikami modelowania (UML + ERD w~Visual Paradigm, W4 pkt 5) i~licencjami (N19 uwaga 6); zmiana SQLite → MySQL po uwadze 1 (Q3), blokady wierszy i~transakcja rezerwacji. |
| Koszt wytworzenia systemu (kosztorys) (3.4) | tabela | Narzędzia 0~zł (licencje open source); praca tylko z~danych od Karola albo jawny szacunek względny. |
| Plan projektu (3.5) | proza lub lista etapów z~rezultatami | — |
| Grupa i~podział obowiązków (3.6) | 3.6.1 tabela składu; 3.6.2 `longtable` obowiązków w~etapach | Na analizie jedna osoba w~roli właściciela, dwie jako analitycy (wywiad). Projekt wspólnie; podział backend/frontend/BD dopiero przy kodzie. Tuż przed harmonogramem. |
| Harmonogram (3.7) | tabela dat 19.10 / 17.11 / 30.11 / 14.12 | Wykres Gantta (`pgfgantt`) tylko na prośbę. |

## Wymagane elementy — etap 2: Faza projektowa (2.3–2.5, rozdz. 4–6)

Struktura funkcjonalna **i** informacyjna (wytyczne pkt 5; dobór technik i~narzędzie Visual Paradigm opisuje 3.3.1; wszystkie diagramy UML i~ERD w~Visual Paradigm):

1. **Wymagania funkcjonalne** (2.3) — `WF01…`, w~kolejności SH: konta, uwierzytelnianie, sprzedawca, właściciel, klient, zalogowany użytkownik, klient-obserwator, proces rezerwacji, każde niepodzielne i~sprawdzalne (wzór: Biblioteka F01–F08, Sklep hydrauliczny 2.2.x). Konta, uwierzytelnianie (reguły haseł), uprawnienia ról.
2. **Wymagania niefunkcjonalne** (2.4) — `WN01…`: platforma (komputer w~sklepie, system, przeglądarka), SZBD i~licencja, współbieżność zapisów, bezpieczeństwo (hasła haszowane, osobny panel klienta), kopia zapasowa, język UI.
3. **Architektura trójwarstwowa** (opisywana w~7.3 „Architektura trójwarstwowa” i~7.4 „Oddzielenie kodu od HTML – szablony Django”, jak SH 6.1.2; projektuje się ją w~etapie 2) — diagram komponentów (prezentacja: szablony Django; kontrola: widoki/serwisy; dane: modele ORM + baza) + akapit, jak Django MTV realizuje pkt 9 wytycznych.
4. **Aktorzy i~diagramy przypadków użycia** — lista aktorów z~opisem, diagram aktorów (z~uogólnieniem), diagramy PU per moduł. Relacje «include» i~«extend» obowiązkowe. Nazwy PU jak czynności („Złożenie rezerwacji”).
5. **Scenariusze PU** — numer i~nazwa, aktor, zdarzenie inicjujące, warunki początkowe, przebieg podstawowy (numerowany), alternatywne (z~numerem kroku), warunki końcowe, spełnione `WFxx`. Przy każdym makieta (`rys.~\ref{}`).
6. **Makiety interfejsu** — po jednej na stan ekranu, nazwa = przeznaczenie okna. Opcjonalnie diagram stanów interfejsu.
7. **Diagram czynności** (5.6) — dla 1–2 najbardziej złożonych PU: partycje = aktorzy, decyzja, fork/join.
8. **Diagram stanów rezerwacji** (6.7) — stany i~przejścia z~opisem (wzór: graf stanów zamówienia, Sklep hydrauliczny 5.7).
9. **Model bazy danych** (rozdz. 6, od 6.1 „Podejście code-first”; nazwa „model bazy danych”, nie „projekt bazy”): encje i~związki → model konceptualny (ERD) → model logiczny (typy) → normalizacja 1NF/2NF/3NF z~uzasadnieniem dla konkretnych tabel → diagram klas modeli ORM.
10. **Słownik danych (definicje obiektów, W4 5b)** (6.6) — `longtable`: tabela, atrybut, typ, ograniczenia (PK, FK, NOT NULL, UNIQUE, CHECK), opis.

## Wymagane elementy — etap 3: Implementacja i~walidacja (rozdz. 7–10)

- Środowisko programistyczne i~repozytorium kodu (7.2; N19 „Ustalenia”: konfiguracja środowiska równolegle z~dokumentacją).

- Technologie z~wersjami (z~`requirements.txt`), uzasadnienie wyboru.
- Struktura projektu (drzewo, aplikacje Django) i~mapowanie na warstwy.
- Model fizyczny: SQL z~`manage.py sqlmigrate` albo listing modelu.
- Fragment kodu z~omówieniem (np. transakcyjna zmiana stanu przy rezerwacji) — listing ≤30 linii + akapit.
- Panel administratora vs panel klienta — co gdzie jest dostępne.
- Testy: tabela (ID, PU/WF, kroki, oczekiwany wynik, wynik). Wyniki **tylko** z~faktycznie uruchomionych testów lub od Karola.
- Zmienione i~niezrealizowane koncepcje, napotkane problemy (wzór: Restauracja 5.4–5.5) — tylko prawdziwe, od zespołu.

## Wymagane elementy — etap 4: Wdrożenie aplikacji (rozdz. 11)

- Środowisko docelowe (komputer w~sklepie: system, Python, sieć) — dane od Karola.
- Instrukcja instalacji krok po kroku (venv, `pip install -r requirements.txt`, `migrate`, `createsuperuser`, `loaddata`, uruchomienie) w~`lstlisting`, sprawdzona na czystym środowisku.
- Dane początkowe i~konta (bez haseł w~treści).
- Kopia zapasowa i~odtwarzanie bazy.
- Podręcznik użytkownika per rola ze zrzutami (wzór: Restauracja 6, Szkółka 7).
- Checklista odbioru (punkt, kryterium, wynik).

## Wymagane elementy — etap 5: Prezentacja i~zaliczenie (rozdz. 12–13)

- Wnioski: co zrealizowano wobec wersji min/std/rozsz., czego nie i~dlaczego, czego się nauczono, rozszerzenia. Konkretnie (wzór: Sklep hydrauliczny rozdz. 10).
- Plan prezentacji (12.1): przebieg demonstracji krótko (lista kroków); slajdy poza raportem.
- Materiały przekazywane do zaliczenia (12.2): dokumentacja, aplikacja na komputerze w~sklepie, repozytorium (W4 pkt 6 „wraz z~dokumentacją”).

## Checklista kompletności sekcji

1. Sekcja pokrywa odpowiadający punkt wytycznych v4 (mapowanie: `docs/plan-sprawozdania.md` §1).
2. Wszystkie fakty pochodzą od Karola, z~notatek, z~kodu albo z~uruchomionych poleceń.
3. Zgodność z~wcześniejszymi sekcjami: te same role, nazwy encji, ID wymagań (`WFxx` ↔ PU ↔ testy).
4. Samokontrola stylu ze skilla `styl-sprawozdania` przeprowadzona.
5. Karol zaakceptował treść; dziennik decyzji w~`CLAUDE.md` zaktualizowany, jeśli w~rozmowie zapadły decyzje.
