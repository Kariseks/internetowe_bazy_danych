# Plan realizacji sprawozdania IBD — lokalny warzywniak

Źródła: `materialy/IDB_wytyczne_v4.pdf` (nadrzędne), notatka z konsultacji 19.10.2026 (`materialy/notatki/notatka_ze_spotkania_19_10_26.md`), przykłady z `materialy/bazdy danych/` i `materialy/io/`, szkielet `dokumentacja/sprawozdanie.tex`. Sposób pisania: `CLAUDE.md` i skille w `.claude/skills/`. Mapa źródeł: `docs/indeks-zrodel.md`.

Stan na 04.11.2026: napisane 1.1, 1.2, 1.3 i 1.5; pozostałe podsekcje puste (szkielet wg §1).

**Decyzja Q1 (03.11.2026, Karol): przyjęty zakres z notatki 19.10.** MVP obejmuje rezerwacje klientów z odbiorem osobistym, konta klientów, klienta-obserwatora (przegląd bez logowania) i osobny panel klienta. Django Admin służy tylko personelowi. Założenie „system tylko dla personelu, klient i dostawca w otoczeniu bez konta” jest nieaktualne.

**Decyzja Q2 (03.11.2026, Karol): etap 1 pisany od nowa.** Dawnej treści z git (`git show HEAD:dokumentacja/rozdzialy/01-analiza.tex`) nie przywraca się i nie wkleja. Statusy ✅ etapu 1 w `PLAN.md` są nieważne. Fakty z dawnej wersji (oznaczone niżej [H01]) wolno użyć dopiero po potwierdzeniu przez Karola w dyskusji nad daną sekcją.

**Tryb pracy (03.11.2026, Karol):** sekcje omawia się z Karolem pojedynczo, w kolejności z §7; tekst do `sprawozdanie.tex` powstaje dopiero po omówieniu.

---

## 1. Struktura sprawozdania i pokrycie wytycznych v4

Stan 04.11.2026 (druga przebudowa): struktura i logika wywodu wzorowane na raporcie „Sklep hydrauliczny” (`materialy/bazdy danych/Sklep hydrauliczny - przykładowy raport.pdf`, dalej SH), uzupełnione o elementy wymagane przez wytyczne v4 i notatkę 19.10, których SH nie ma. Rozdziały = `\section`, każdy od nowej strony. Kopie: `dokumentacja/sprawozdanie.pre-restructure.tex.bak` (przed pierwszą przebudową), `dokumentacja/sprawozdanie.pre-restructure2.tex.bak` (przed drugą).

### Wzorzec SH (do wglądu)

Raport z kursu „Bazy danych” (dr inż. P. Rogaliński), 102 s. PDF; strony podano wg numeracji PDF (drukowana = PDF − 2).

```
Strona tytułowa, Spis treści (s. 1–5)
Specyfikacja projektu (bez numeru, s. 7–8): cel w 3 zdaniach; „Wykorzystane technologie i narzędzia” (lista 8 pozycji);
    „Główne funkcjonalności aplikacji” (5 punktów); „Uwagi dodatkowe” (2 zdania o Dockerze). Streszczenie, bez nowych faktów.
1 Opis świata rzeczywistego (s. 9–10, bez podrozdziałów): proza o działalności hurtowni i obecnym sposobie wydawania towaru
    instalatorom (wydanie zewnętrzne, zwroty, faktura), kto może z tego korzystać; czynności pracownika i prezesa (statystyki);
    dane klientów i pracowników; lista stanów zamówienia; „Obecnie asortyment… na stronie”; atrybuty produktu
    (kod, cena, nazwa, zdjęcie, jednostka, minimalny próg). Czyli: jak jest + reguły dziedziny, na których system się oprze.
2 Cel projektu oraz wymagania systemu (s. 11–14)
  2.1 Cel projektu — co system ma wspierać i komu; forma (strona WWW), dostęp bez konta; „Uwaga:” czego system nie robi
  2.2 Wymagania funkcjonalne — 2.2.1 Konta użytkowników; 2.2.2 Identyfikacja i uwierzytelnianie (hasło, 2FA symulowane);
      2.2.3 pracownik; 2.2.4 kierownik; 2.2.5 klient; 2.2.6 zalogowany użytkownik; 2.2.7 niezalogowany użytkownik;
      2.2.8 Funkcje wymagane do obsługi procesu zamówienia (numerowane kroki z „(opcjonalnie)”)
  2.3 Wymagania niefunkcjonalne (4 punkty: SQL z darmową licencją, terminale, przeglądarka i RAM, GUI)
  2.4 Funkcjonalności implementowane i testowane na zaliczenie — 2.4.1 minimalna, 2.4.2 standardowa, 2.4.3 rozszerzona
3 Diagramy przypadków użycia (s. 15–19) — 3.1 Identyfikacja aktorów (lista + rysunek); 3.2 diagramy dla modułów
    (Administracja, Hurtownia, Sklep internetowy)
4 Opis przypadków użycia (s. 21–52) — 4.1 poprawione diagramy PU z opisem zmian; 4.2–4.5 PU wg aktorów (gość, użytkownik,
    pracownik, kierownik): makiety ekranów + aktor, zdarzenie inicjujące, warunki początkowe, przebieg podstawowy
    i alternatywny, warunki końcowe; 4.6 Grafiki (poprzednie wersje diagramów)
5 Modele bazy danych (s. 53–66) — wstęp: tabela postaci normalnych 1NF–3NF; 5.1–5.6 kolejne wersje modelu
    (ERD, konceptualny, fizyczny) z oceną NF; 5.7 Graf stanów zamówienia (rysunek + numerowana lista stanów i przejść)
6 Opis implementacji (s. 69–70) — 6.1.1 Technologie; 6.1.2 Struktura systemu (warstwy: repozytoria, serwisy, prezentacja);
    6.1.3 Moduły funkcjonalne; 6.1.4 Model danych (lista encji); 6.1.5 Bezpieczeństwo
7 Główne moduły i klasy (s. 71–73) — pakiety 7.1.1–7.1.9 z klasami i jednym zdaniem opisu; 7.1.10 Testy; 7.1.11 Pozostałe pliki
8 Opis wybranego fragmentu kodu źródłowego (s. 75–85) — klasa usługi zamówień: konstruktor, tworzenie zamówienia,
    akceptacja/odrzucenie, kompletowanie, odbiór i opłata, zwrot, metody pomocnicze (listingi + komentarz)
9 Podręcznik dla użytkownika (s. 87–98) — 9.1 Uruchomienie aplikacji (tryb deweloperski, budowanie, Docker, baza, dostęp);
    9.2 Przewodnik po rolach (gość, klient, pracownik, kierownik — zrzuty ekranów z opisem)
10 Wnioski (s. 99) — 5 numerowanych punktów: czego nie zrobiono, co dalej, lekcja o iteracyjnym modelu danych
Literatura, Spis rysunków (s. 101–102)
```

Logika SH: **jak jest** (rozdz. 1) → **po co system i co ma robić** (2.1 cel, wyłączenia) → **wymagania** (2.2–2.4) → **przypadki użycia** (3–4) → **baza danych** (5) → **implementacja** (6–8) → **podręcznik** (9) → **wnioski** (10). SH nie ma SWOT, CSF, wykonalności, kosztu, planu, harmonogramu, podziału obowiązków, parametrów skalowalnych ani testów jako rozdziału — to dochodzi z wytycznych v4 (kurs IBD) i z przykładów ROW/RE/IO.

### Szkielet

Stan 04.11.2026 (trzecia korekta): każdy element wytycznych v4 i notatki 19.10 ma własny nagłówek o nazwie bliskiej brzmieniu wytycznych (★ = punkt dodany albo przemianowany w tej korekcie).

```
Specyfikacja projektu (bez numeru) — TODO na koniec            [SH Specyfikacja]       sec:specyfikacja
1 Opis słowny świata rzeczywistego ★nazwa                         [SH 1 + W4 4b]          ch:swiat
  1.1 Obecny sposób działania sklepu         (jak jest)          [NAPISANE] sec:opis
  1.2 Problemy prowadzenia sklepu bez systemu (dlaczego system)  [NAPISANE] sec:problemy, prob:* (P1–P8)
  1.3 Proponowany system                     (co wprowadza)      [NAPISANE] sec:system
  1.4 Interesariusze i otoczenie podsystemu ★nazwa                [NAPISANE] sec:otoczenie, tab:otoczenie
  1.5 Parametry skalowalne                                       [NAPISANE] sec:parametry, tab:parametry
2 Cel projektu oraz wymagania systemu                            [SH 2]                  ch:cel
  2.1 Cel projektu ★                                                        sec:cel
  2.2 Zakres projektu ★                                                     sec:zakres
  2.3 Wymagania funkcjonalne                                                sec:wf
      2.3.1 Konta użytkowników  2.3.2 Identyfikacja i uwierzytelnianie  2.3.3 sprzedawca  2.3.4 właściciel
      2.3.5 klient  2.3.6 zalogowany użytkownik  2.3.7 klient-obserwator  2.3.8 proces rezerwacji
  2.4 Wymagania niefunkcjonalne                                             sec:wn
  2.5 Funkcjonalności implementowane i testowane na zaliczenie (min / std / rozsz.)   sec:wersje
3 Uzasadnienie potrzeby realizacji i organizacja projektu ★nazwa  [W4 4a–4e, etap 1]     ch:uzasadnienie
  3.1 Analiza SWOT  3.2 Czynniki krytyczne sukcesu (CSF)
  3.3 Techniczna wykonalność systemu ★nazwa                                 sec:wykonalnosc
      3.3.1 Wybór technologii, wersje i licencje ★  3.3.2 Współbieżne zapisy w bazie SQLite ★
  3.4 Koszt wytworzenia systemu (kosztorys) ★nazwa                          sec:koszt
  3.5 Plan projektu
  3.6 Grupa projektowa i podział obowiązków                                 sec:grupa
      3.6.1 Skład grupy ★  3.6.2 Podział obowiązków w etapach projektu ★
  3.7 Harmonogram
4 Techniki modelowania ★                                         [W4 pkt 5]              ch:techniki
  4.1 Dobór technik modelowania i diagramów ★  4.2 Struktura funkcjonalna i informacyjna systemu ★
5 Diagramy przypadków użycia                                     [SH 3]                  ch:diagramy-pu
  5.1 Identyfikacja aktorów  5.2 Diagramy przypadków użycia dla poszczególnych modułów
6 Opis przypadków użycia                                         [SH 4]                  ch:opis-pu
  6.1–6.4 PU dla klienta-obserwatora / klienta / sprzedawcy / właściciela (makiety + scenariusze)
  6.5 Diagramy czynności wybranych przypadków użycia ★ (Q4 — usunąć, jeśli Karol nie wybierze)
7 Model bazy danych                                              [SH 5; N19 uwaga 6]     ch:model-bd
  7.1 Podejście code-first ★  7.2 Identyfikacja encji i związków  7.3 Model konceptualny (ERD) ★nazwa
  7.4 Model logiczny i normalizacja  7.5 Diagram klas modeli ORM  7.6 Słownik danych (definicje obiektów) ★nazwa
  7.7 Graf stanów rezerwacji
8 Opis implementacji                                             [SH 6; W4 7–9]          ch:implementacja
  8.1 Technologie  8.2 Środowisko programistyczne i repozytorium kodu ★
  8.3 Architektura trójwarstwowa ★nazwa (sec:architektura)  8.4 Oddzielenie kodu od HTML – szablony Django ★
  8.5 Moduły funkcjonalne  8.6 Panel klienta i panel administratora  8.7 Model fizyczny bazy danych ★nazwa  8.8 Bezpieczeństwo
9 Główne moduły i klasy                                          [SH 7]                  ch:moduly
  9.1 Aplikacje Django i modele  9.2 Widoki i szablony panelu klienta  9.3 Konfiguracja panelu administratora  9.4 Pozostałe pliki
10 Opis wybranego fragmentu kodu źródłowego                      [SH 8]                  ch:kod
11 Walidacja i testy                                             [etap 3; IO, RE 5.4–5.5] ch:testy
  11.1 Testy jednostkowe  11.2 Testy akceptacyjne PU  11.3 Zmienione i niezrealizowane koncepcje, napotkane problemy
12 Wdrożenie aplikacji i podręcznik dla użytkownika ★nazwa        [SH 9; etap 4]          ch:wdrozenie
  12.1 Uruchomienie aplikacji: 12.1.1 Środowisko uruchomieniowe w sklepie ★nazwa
       12.1.2 Instrukcja instalacji na komputerze w sklepie ★nazwa  12.1.3 Dane początkowe i konta
       12.1.4 Kopia zapasowa i odtwarzanie  12.1.5 Dostęp do aplikacji
  12.2 Przewodnik po rolach użytkowników (4 role)  12.3 Checklista odbioru
13 Prezentacja i zaliczenie projektu ★nazwa                       [W4 pkt 6, etap 5]      ch:prezentacja
  13.1 Plan prezentacji ★  13.2 Materiały przekazywane do zaliczenia ★
14 Wnioski                                                       [SH 10]                 ch:wnioski
(Literatura, Spis rysunków — jak w SH; decyzja Q14)
```

Etapy wytycznych → rozdziały: etap 1 → rozdz. 1, 2.1–2.2, 3 (WF/WN domyka się w fazie projektowej, zgodnie z „Ustaleniami” notatki 19.10); etap 2 → 2.3–2.5, rozdz. 4–7; etap 3 → rozdz. 8–11; etap 4 → rozdz. 12; etap 5 → rozdz. 13–14.

**Wzięte z SH:** nienumerowana Specyfikacja; rozdz. 1 jako opis świata, który zawiera także reguły dziedziny, na których oprze się system; tytuł i układ rozdz. 2 (cel z „Uwagą”, WF w kolejności SH, WN, wersje); diagramy PU i opis PU wg aktorów; rozdział bazy zakończony grafem stanów; rozdział implementacji z architekturą warstwową i modelem danych; moduły i klasy; fragment kodu; podręcznik z „Uruchomieniem aplikacji” i przewodnikiem po rolach; wnioski.

**Własne (wymagane przez W4/N19 albo decyzje Karola):** w rozdz. 1 podział na jak jest → problemy P1–P8 → proponowany system → otoczenie podsystemu → parametry skalowalne; osobne „Cel projektu” i „Zakres projektu” (W4 4d); rozdz. 3 z SWOT, CSF, techniczną wykonalnością (z wyborem technologii i ryzykiem SQLite), kosztorysem, planem, grupą tuż przed harmonogramem; rozdz. 4 „Techniki modelowania” (W4 pkt 5); diagramy czynności (Q4); „Podejście code-first” i „Słownik danych (definicje obiektów)” w modelu bazy; środowisko programistyczne, architektura trójwarstwowa i szablony jako osobne podrozdziały implementacji (W4 pkt 9); rozdział testów (walidacja); instalacja na komputerze w sklepie, kopia, checklista odbioru; rozdział prezentacji i zaliczenia.

### Pokrycie wymagań

★ = sekcja dodana lub przemianowana 04.11.2026 (trzecia korekta), żeby wymóg miał własny, rozpoznawalny nagłówek.

| Wymóg | Sekcja w `sprawozdanie.tex` |
|---|---|
| W4 pkt 2 Grupy ok. 3-osobowe | 3.6.1 Skład grupy ★ |
| W4 pkt 3 Tematyka „biznesowa” | 1 Opis słowny świata rzeczywistego (sklep jako działalność gospodarcza), Specyfikacja projektu |
| W4 4a Dobór grupy | 3.6 Grupa projektowa i podział obowiązków, 3.6.1 Skład grupy ★ |
| W4 4a Ustalenie podziału obowiązków | 3.6.2 Podział obowiązków w etapach projektu ★ |
| W4 4b Opis słowny | 1 Opis słowny świata rzeczywistego ★ (1.1 Obecny sposób działania sklepu, 1.3 Proponowany system) |
| W4 4b Analiza SWOT | 3.1 Analiza SWOT |
| W4 4b Analiza celów | 2.1 Cel projektu ★ |
| W4 4b Analiza problemów | 1.2 Problemy prowadzenia sklepu bez systemu |
| W4 4b CSF | 3.2 Czynniki krytyczne sukcesu (CSF) |
| W4 4b Otoczenie podsystemu | 1.4 Interesariusze i otoczenie podsystemu ★ |
| W4 4c Plan projektu (ogólny) | 3.5 Plan projektu |
| W4 4d Cel | 2.1 Cel projektu ★ |
| W4 4d Zakres | 2.2 Zakres projektu ★ (+ 2.5 wersje) |
| W4 4d Techniczna wykonalność systemu | 3.3 Techniczna wykonalność systemu ★ |
| W4 4d Koszt wytworzenia | 3.4 Koszt wytworzenia systemu (kosztorys) ★ |
| W4 4e Harmonogram | 3.7 Harmonogram |
| W4 pkt 5 Dobór technik modelowania | 4.1 Dobór technik modelowania i diagramów ★ |
| W4 pkt 5e Struktura funkcjonalna i informacyjna | 4.2 Struktura funkcjonalna i informacyjna systemu ★ |
| W4 5a UML — diagramy PU | 5 Diagramy przypadków użycia |
| W4 5a UML — scenariusze PU | 6.1–6.4 Przypadki użycia dla … |
| W4 5a UML — diagram czynności | 6.5 Diagramy czynności wybranych przypadków użycia ★ (Q4) |
| W4 5a UML — diagram klas | 7.5 Diagram klas modeli ORM |
| W4 5a UML — diagram stanów | 7.7 Graf stanów rezerwacji |
| W4 5b ERD | 7.3 Model konceptualny (ERD) ★, 7.4 Model logiczny i normalizacja |
| W4 5b Definicje obiektów | 7.6 Słownik danych (definicje obiektów) ★ |
| W4 5c–d DHF, DNF, DFE | nie wybrano; uzasadnienie w 4.1 ★ |
| W4 pkt 6 Prezentacja wraz z dokumentacją | 13 Prezentacja i zaliczenie projektu ★: 13.1 Plan prezentacji ★, 13.2 Materiały przekazywane do zaliczenia ★ |
| W4 pkt 7–8 Technologie | 3.3.1 Wybór technologii, wersje i licencje ★, 8.1 Technologie |
| W4 pkt 9 Architektura trójwarstwowa | 8.3 Architektura trójwarstwowa ★ |
| W4 pkt 9 Oddzielenie kodu od HTML przez szablony | 8.4 Oddzielenie kodu od HTML – szablony Django ★, 9.2 Widoki i szablony panelu klienta |
| W4 etap 1 Przygotowanie i uzasadnienie potrzeby realizacji | 3 Uzasadnienie potrzeby realizacji i organizacja projektu ★ |
| W4 etap 1 Analiza problemu | 1.2 Problemy prowadzenia sklepu bez systemu |
| W4 etap 2 Faza projektowa | 2.3–2.5, 4–7 |
| W4 etap 3 Implementacja | 8 Opis implementacji, 9 Główne moduły i klasy, 10 Opis wybranego fragmentu kodu |
| W4 etap 3 Walidacja | 11 Walidacja i testy |
| W4 etap 4 Wdrożenie aplikacji | 12 Wdrożenie aplikacji i podręcznik dla użytkownika ★ |
| W4 etap 5 Prezentacja i zaliczenie całości | 13 Prezentacja i zaliczenie projektu ★, 14 Wnioski |
| N19 zakres: rezerwacje ilości, odbiór osobisty, bez dowozu i płatności online | 2.2 Zakres projektu ★, 1.3, 2.3.8 |
| N19 uwaga 1: SQLite a współbieżne zapisy | 3.3.2 Współbieżne zapisy w bazie SQLite ★ |
| N19 uwaga 2: klient-obserwator | 2.3.7 Funkcje dostępne dla klienta-obserwatora, 6.1, 12.2.1 |
| N19 uwaga 3: Django Admin tylko dla personelu, osobny panel klienta | 8.6 Panel klienta i panel administratora |
| N19 uwaga 4: wywiad (właściciel + analitycy), wspólne projektowanie, podział przy kodowaniu | 3.6.2 Podział obowiązków w etapach projektu ★ |
| N19 uwaga 5: poprawki SWOT | 3.1 Analiza SWOT |
| N19 uwaga 6: konkretne wersje Django i Pythona, licencje | 3.3.1 Wybór technologii, wersje i licencje ★, 8.1 |
| N19 uwaga 6: kosztorys z 0 zł za narzędzia | 3.4 Koszt wytworzenia systemu (kosztorys) ★ |
| N19 uwaga 6: „model bazy danych” z klas ORM (code-first) | 7 Model bazy danych, 7.1 Podejście code-first ★, 7.5 |
| N19 uwaga 6: instrukcja instalacji na komputerze w sklepie | 12.1.2 Instrukcja instalacji na komputerze w sklepie ★ |
| N19 ustalenia: konfiguracja środowiska i prosta działająca wersja | 8.2 Środowisko programistyczne i repozytorium kodu ★ |
| N19 ustalenia: zamknięcie fazy projektowej (WF/WN, PU, klasy ORM, SWOT, kosztorys) | 2.3, 2.4, 5, 7.5, 3.1, 3.4 |

Luki: brak. Otwarte: diagram czynności (6.5) i ewentualny diagram stanów interfejsu zależą od Q4; Literatura i spis rysunków — Q14.

Drobne poprawki LaTeX (też do akceptacji): makro `\figura` z trzecim argumentem `\label`; opcjonalnie `\listoffigures` na końcu, tak jak w przykładach.

---

## 2. Plan per sekcja

Tabele poniżej są pogrupowane wg etapów wytycznych; numery sekcji w szkielecie podaje §1 (etap 1 → rozdz. 1, 2.1–2.2 i 3; etap 2 → 2.3–2.5 i rozdz. 4–7; etap 3 → rozdz. 8–11; etap 4 → rozdz. 12; etap 5 → rozdz. 13–14).

Legenda: **Treść**, **Rys./Tab.**, **Od Karola**, **Zależy od** (numer pytania z §5).

### Etap 1 — Przygotowanie i uzasadnienie (termin 19.10 minął; pisany od nowa wg Q2, kolejność omawiania w §7)

| Sekcja | Treść | Rys./Tab. | Od Karola | Zależy od |
|---|---|---|---|---|
| Grupa i obowiązki | skład, obowiązki ogólne i etapowe; role z wywiadu (właściciel i analitycy) | tab. skład, `longtable` obowiązków | kto był „właścicielem” w wywiadzie; czy podział z PLAN zostaje | Q12 |
| Opis słowny | sklep, asortyment, dostawy, sprzedaż przy ladzie, rezerwacje z odbiorem osobistym, role: właściciel, sprzedawca, dostawca, klient, klient-obserwator | — | szczegóły rezerwacji, godziny pracy, liczba personelu | Q7 |
| Parametry skalowalne | liczba produktów, kont, rezerwacji i sprzedaży dziennie, sezonowość | lista | wszystkie liczby | — |
| Problemy bez systemu | psucie towaru (N19); nieznany stan („pamięć albo kartki”, H01); obecny sposób rezerwacji — brak w źródłach | lista | obecny sposób rezerwacji, inne problemy | — |
| Interesariusze | tabela ról, w tym klient z kontem i klient-obserwator | tab. | — | — |
| SWOT | poprawki prowadzącego: krótki czas wdrożenia → słabe strony; błędy techniczne → zagrożenia; usunąć „brak kodu” | tab. 2×2 lub 4 wiersze | punkty SWOT od zespołu, akceptacja | — |
| CSF | aktualizacja o rezerwacje (stan nie ujemny po rezerwacji, odbiór) | tab. | — | — |
| Cel, zakres, wersje | cel biznesowy: mniej strat; w zakresie / poza zakresem (dowóz, płatność online) | tab. zakresu, lista wersji | które funkcje są w wersji min/std/rozsz. | Q8 |
| Koszt wytworzenia | narzędzia 0 zł (licencje), sprzęt istniejący w sklepie, praca | tab. kosztów | godziny/stawka albo zgoda na szacunek względny | Q9 |
| Wykonalność | Django, Python, SQLite/MySQL z wersjami; ryzyko współbieżnych zapisów | — | wersje (lub `requirements.txt`) | Q3, Q10 |
| Plan i harmonogram | etapy i daty, rezultaty | tab. harmonogramu | — | — |

### Etap 2 — Faza projektowa (termin 17.11)

| Sekcja | Treść | Rys./Tab. | Od Karola | Zależy od |
|---|---|---|---|---|
| Wymagania funkcjonalne | `WF01…` wg ról: gość (przegląd oferty i stanów), klient (rejestracja, logowanie, złożenie/anulowanie rezerwacji, historia), sprzedawca (dostawa, sprzedaż, realizacja rezerwacji), właściciel (produkty, ceny, konta, raporty) | lista numerowana | reguły haseł, czas ważności rezerwacji, limity | Q7 |
| Wymagania niefunkcjonalne | `WN01…`: platforma, SZBD i licencja, współbieżność, bezpieczeństwo, kopia, UI po polsku | lista | sprzęt w sklepie, dostęp klientów (LAN/internet) | Q3, Q6 |
| Architektura | MTV jako 3 warstwy; panel admina vs panel klienta | diagram komponentów | — | Q4 |
| Aktorzy i PU | aktorzy z uogólnieniem; moduły: Oferta i rezerwacje, Magazyn i sprzedaż, Administracja; «include»/«extend» | diagram aktorów, 3 diagramy PU | narzędzie do diagramów | Q4, Q5 |
| Scenariusze PU | format: aktor, zdarzenie inicjujące, warunki początkowe, przebieg podstawowy i alternatywny, warunki końcowe, `WFxx` | makiety (1 na ekran) | akceptacja listy PU | — |
| Diagram czynności | „Złożenie rezerwacji” i „Realizacja/odbiór rezerwacji” | 2 diagramy | — | Q4 |
| Diagram stanów | rezerwacja wg Q7 i 1.3: złożona → przygotowana do odbioru → odebrana (stan „przygotowana” do akceptacji, CLAUDE.md pkt 37); złożona → odebrana; złożona → anulowana (do 18:00 dnia poprzedniego); złożona → nieodebrana (po 18:00 dnia odbioru, naliczenie opłaty 10%) | diagram + opis stanów | akceptacja uzupełnień Q7 | — |
| Model bazy | encje: Produkt, (Kategoria), Dostawca, Dostawa, PozycjaDostawy, Sprzedaż, PozycjaSprzedaży, Rezerwacja, PozycjaRezerwacji, Użytkownik/Klient (+ role przez grupy Django); konceptualny → logiczny → 1–3NF; diagram klas ORM | ERD konceptualny, ERD logiczny, diagram klas | notacja ERD, nazwy PL/EN, sposób liczenia stanu | Q4, Q5, Q11 |
| Słownik danych | atrybut, typ, ograniczenia, opis | `longtable` | — | Q11 |

### Etap 3 — Implementacja i walidacja (termin 30.11)

| Sekcja | Treść | Rys./Tab. | Od Karola | Zależy od |
|---|---|---|---|---|
| Stack | wersje z `requirements.txt`, licencje, uzasadnienie | tab. technologii | — | Q3 |
| Struktura | drzewo projektu, aplikacje Django → warstwy | listing drzewa | kod w repo | — |
| Modele i model fizyczny | modele, migracje, SQL z `sqlmigrate` | listing | — | Q11 |
| Widoki i szablony | panel klienta: katalog, rezerwacje, konto | zrzuty | zrzuty z działającej aplikacji | — |
| Panel admina | rejestracje modeli, uprawnienia grup | zrzut | — | — |
| Fragment kodu | transakcyjna zmiana stanu przy rezerwacji i sprzedaży | listing ≤30 linii | — | Q3 |
| Testy | `manage.py test` + testy ręczne PU | tab. testów (ID, PU/WF, wynik) | wyniki uruchomień | — |
| Zmiany i problemy | rzeczywiste odstępstwa od projektu | lista | relacja zespołu | — |

### Etap 4 — Wdrożenie (termin 30.11)

| Sekcja | Treść | Rys./Tab. | Od Karola | Zależy od |
|---|---|---|---|---|
| Środowisko | komputer w sklepie: system, Python, sieć, dostęp klientów | tab. | parametry sprzętu | Q6 |
| Instrukcja | venv, pip, migrate, createsuperuser, loaddata, uruchomienie (serwer WSGI albo runserver), autostart | listingi bash | system docelowy | Q6 |
| Dane i konta | fixtures asortymentu, konta demo (bez haseł) | tab. | lista produktów startowych | — |
| Kopia | kopia `db.sqlite3` / `dumpdata`, odtworzenie | listing | — | Q3 |
| Podręcznik | per rola: gość, klient, sprzedawca, właściciel | zrzuty | zrzuty | — |
| Checklista odbioru | punkty odbioru i wynik | tab. | wynik odbioru | — |

### Etap 5 — Prezentacja i zaliczenie (termin 14.12)

| Sekcja | Treść | Od Karola |
|---|---|---|
| Przebieg prezentacji | kolejność demonstracji, kto pokazuje | podział wypowiedzi |
| Wnioski | realizacja wersji min/std/rozsz., problemy, rozszerzenia | ocena zespołu |

---

## 3. Kolejność prac względem terminów

1. **Teraz → 10.11 (odblokowanie):** decyzje Q3–Q5 (Q1 i Q2 rozstrzygnięte). Napisać etap 1 od nowa, sekcja po sekcji w kolejności z §7 (zakres z konsultacji, poprawiony SWOT, wersje, koszt). Zaakceptować nowy szkielet.
2. **10.11 → 17.11 (projekt):** WF/WN → aktorzy i diagramy PU → scenariusze + makiety → architektura → ERD konceptualny i logiczny + normalizacja → diagram klas ORM i słownik → diagram stanów i czynności. Równolegle: szkielet projektu Django i modele, bo diagram klas ORM i ERD powstają z kodu (code-first).
3. **17.11 → 30.11 (implementacja i wdrożenie):** widoki klienta, panel admina, logika stanu i rezerwacji, testy, instalacja na docelowym komputerze, kopia, zrzuty ekranu. Sekcje 3 i 4 piszą się z kodu i z wyników.
4. **30.11 → 14.12 (prezentacja):** podręcznik użytkownika, wnioski, zmiany i problemy, korekta całości wg checklist ze skilli `zrodla-sprawozdania` i `styl-sprawozdania`, ostateczny PDF.

Szkielet przebudowano 04.11.2026, drugi raz tego samego dnia ściślej wg SH (§1). Kolejka `PLAN.md` (1.x–5.x) jest nieaktualna i czeka na przebudowę pod nowy szkielet (Q12).

---

## 4. Minimum aplikacji Django, które raport ma opisać

Szczegóły i kolejność budowy: §6.

- **Modele:** Produkt (nazwa, jednostka, cena, stan albo stan liczony z ruchów, aktywny), opcjonalnie Kategoria; Dostawca; Dostawa i PozycjaDostawy; Sprzedaż i PozycjaSprzedaży; Rezerwacja (klient, data, termin odbioru, status) i PozycjaRezerwacji; konto klienta (`User` + profil); role personelu przez grupy i uprawnienia Django.
- **Reguły:** stan nie schodzi poniżej zera; rezerwacja blokuje ilość; dostawa zwiększa stan, sprzedaż i odbiór rezerwacji go zmniejszają; zmiany w `transaction.atomic`; przejścia statusów zgodne z diagramem stanów.
- **Panel klienta (osobny od admina):** publiczny katalog z dostępnością bez logowania (klient-obserwator), rejestracja, logowanie, złożenie i anulowanie rezerwacji, „moje rezerwacje”.
- **Panel personelu:** Django Admin dla właściciela i sprzedawcy: produkty, ceny, dostawy, sprzedaż, lista rezerwacji ze zmianą statusu.
- **Szablony Django:** oddzielenie HTML od logiki (wymóg pkt 9).
- **Testy:** `TestCase` dla reguł stanu i rezerwacji, testy widoków głównych PU.
- **Wdrożenie:** `requirements.txt` z wersjami, fixtures z danymi początkowymi, `DEBUG=False` i `ALLOWED_HOSTS` dla komputera w sklepie, procedura kopii bazy.

---

## 5. Pytania i decyzje dla Karola (od najbardziej blokujących)

1. ~~**Zakres po konsultacji 19.10.**~~ **ROZSTRZYGNIĘTE 03.11.2026: TAK.** W MVP są rezerwacje z odbiorem osobistym, konta klientów, klient-obserwator i osobny panel klienta; admin tylko dla personelu.
2. ~~**Utracona treść etapu 1.**~~ **ROZSTRZYGNIĘTE 03.11.2026: pisać od nowa.** Treści z `git HEAD` (`rozdzialy/01-analiza.tex`) nie przywraca się ani nie wkleja; statusy ✅ etapu 1 w `PLAN.md` są nieważne.
3. ~~**SQLite czy MySQL.**~~ **ROZSTRZYGNIĘTE 04.11.2026: wariant (c) — SQLite, MySQL/MariaDB jako opisana ścieżka rozwoju.** Wytyczne pkt 7 tylko *zalecają* Python + MySQL, a pkt 8 dopuszcza inne technologie; notatka 19.10 zawiera ostrzeżenie (uwaga 1), nie wymóg, i zostawia temat „do głębszego przemyślenia”. Obciążenie z `tab:parametry` (2 os. personelu + do 20 klientów naraz, do 45 rezerwacji i ok. 220 sprzedaży dziennie, jeden komputer w sklepie) to pojedyncze zapisy na minutę; SQLite szereguje zapisy blokadą bazy (to jest kolejkowanie zaproponowane na konsultacji). Warunki do opisania w 3.3.2 i spełnienia w kodzie: tryb WAL, transakcje `IMMEDIATE` i `timeout` w `DATABASES['OPTIONS']`, krótkie transakcje, sprawdzenie dostępnej ilości i zapis rezerwacji w jednej transakcji (wyklucza przekroczenie planu dostawy także przy rezerwacjach tuż przed 18:00). Pierwotne pytanie: Wytyczne zalecają Python + MySQL. Prowadzący ostrzegł przed SQLite przy jednoczesnych zapisach, a rezerwacje klientów przez sieć oznaczają wielu piszących. Warianty: (a) SQLite z uzasadnieniem (mały ruch, jeden komputer, tryb WAL, krótkie transakcje) i opisem ryzyka; (b) MySQL/MariaDB — w Django to zmiana `DATABASES`, raport zyskuje zgodność z zaleceniem; (c) SQLite teraz, MySQL jako opisana ścieżka rozwoju. Który?
4. **Techniki modelowania (wytyczne pkt 5).** Proponowany zestaw: UML (aktorzy, PU per moduł, scenariusze z makietami, czynności dla 1–2 PU, stany rezerwacji, komponenty, klasy modeli ORM) + ERD (konceptualny i logiczny) + normalizacja. DHF/DNF/DFE pomijamy. Zgoda? Czy któryś diagram ma odpaść (np. czynności), żeby zmieścić się do 17.11?
5. **Notacja i narzędzie diagramów.** Przykłady BD używają ERD w notacji Chena (konceptualny) i logicznego ERD; przykłady IO używają Visual Paradigm. Którą notację ERD wybieramy (Chen czy „kurza stopka”) i jakie narzędzie (draw.io, PlantUML, Visual Paradigm)? Dla code-first: czy ERD i diagram klas generujemy z modeli (np. `django-extensions graph_models`)?
6. **Wdrożenie i dostęp klientów.** System ma działać na komputerze w sklepie, bez hostingu. Jak klienci rezerwują z domu? Warianty: tylko w sieci lokalnej (np. tablet przy ladzie), udostępnienie komputera w internecie (przekierowanie portów lub tunel) albo jednak tani hosting. Jaki system operacyjny i sprzęt ma ten komputer?
7. ~~**Reguły rezerwacji.**~~ **ROZSTRZYGNIĘTE 04.11.2026** (fakty od Karola + uzupełnienia agenta; pełna lista w `CLAUDE.md`, dziennik decyzji). Od Karola: sklep czynny codziennie 6:00–18:00; właściciel Jan Nowak (JDG); krajowe warzywa i owoce bez zmian sezonowych, wszystko na wagę; jeden dostawca, dostawa codziennie o 4:00; rezerwacje tylko z towaru dostępnego w dniu odbioru; rezerwacja do 7 dni naprzód (zwykle na następny dzień), limit 20 kg (jedna skrzynka); odbiór do 18:00 dnia odbioru; nieodebranie = utrata zadatku 10% wartości; rejestracja z kartą płatniczą, zadatek pobierany po fakcie; blokada nowych rezerwacji przy zaległości > 100 zł. Agent uzupełnił: plan dostawy jako pula rezerwacji, zamknięcie zapisów i bezpłatne anulowanie do 18:00 dnia poprzedniego, jedna rezerwacja na klienta na dzień, rozliczanie zaległości i zniesienie blokady, dostawca bez konta (wszystko do akceptacji Karola).
8. **Wersje min/std/rozsz.** Przykłady je mają, wytyczne nie wymagają. Dodajemy? Proponowany podział: min = produkty, stany, dostawy, sprzedaż w adminie; std = panel klienta z rezerwacjami; rozsz. = raporty i statystyki, wygasanie rezerwacji, powiadomienia.
9. **Koszt wytworzenia.** Wytyczne wymagają kosztu. Narzędzia: 0 zł (licencje). Praca: podasz godziny i stawkę, czy zostawiamy szacunek względny z jawnym zastrzeżeniem? Czy liczymy sprzęt w sklepie jako istniejący (0 zł)?
10. **Wersje technologii.** Notatka wymaga konkretnych wersji. Które wersje Pythona i Django (np. Django 5.2 LTS)? Czy zapisujemy je dopiero po utworzeniu `requirements.txt`?
11. **Nazewnictwo i model stanu.** Modele PL (`Produkt`, `Rezerwacja`) czy EN (`Product`, `Reservation`)? Czy stan to pole ilości aktualizowane transakcyjnie, czy wartość liczona z ruchów (dostawy − sprzedaż − rezerwacje)? To wpływa na ERD, normalizację i kod.
12. **Zmiana szkieletu i `PLAN.md`.** **Szkielet ZROBIONY 04.11.2026** — `sprawozdanie.tex` przebudowano na wzór „Sklepu hydraulicznego” (14 rozdziałów po korekcie wg wytycznych, patrz §1; kopie przed zmianami: `dokumentacja/sprawozdanie.pre-restructure.tex.bak` i `dokumentacja/sprawozdanie.pre-restructure2.tex.bak`). **Otwarte:** przebudowa kolejki `PLAN.md` z przypisaniem osób. Pierwotne pytanie: czy akceptujesz nowy szkielet z §1 (nowe: parametry skalowalne, wersje, scenariusze z makietami, diagramy czynności i stanów, „Model bazy danych”, model fizyczny, fragment kodu, zmiany i problemy, podręcznik; scalenie podsekcji etapu 5)? Czy przebudować kolejkę `PLAN.md` pod ten szkielet, z przypisaniem osób (prowadzący zalecił wspólną pracę przy projekcie)?
13. ~~**Sprzątanie instrukcji agenta.**~~ **ZROBIONE 03.11.2026.** Instrukcje przeniesiono do `CLAUDE.md` i `.claude/skills/`; `cursor.md`, `SKILL.md` i generyczny szablon `sprawozdanie-pwr-latex` usunięto (do odzyskania z git).
14. **Literatura i spis rysunków.** Dodać krótką bibliografię (dokumentacja Django, SQLite, UML) i `\listoffigures` jak w przykładach?

---

## 6. Plan aplikacji i opis systemu

Zbudowane wyłącznie ze źródeł z `docs/indeks-zrodel.md`. Oznaczenia: **[N19]** notatka 19.10 · **[H01]** dawny etap 1 z git HEAD (sprzed konsultacji; wg Q2 nie wklejać, fakt wolno użyć dopiero po potwierdzeniu przez Karola) · **[W4]** wytyczne v4 · **[PLAN]** `PLAN.md` · **[wzór: …]** forma z przykładu · **[ZAŁ.]** założenie agenta, nie ze źródła — wymaga akceptacji Karola · **⛔** brak w źródłach.

### 6.1 Opis systemu i stan przed wdrożeniem

- Mały, stacjonarny sklep z warzywami i owocami [N19 §1]; jeden punkt, bez sprzedaży wysyłkowej i lojalności [H01 § Opis słowny].
- Sprzedaż detaliczna przy ladzie; produkty na wagę lub na sztuki, z nazwą, jednostką i aktualną ceną; asortyment zmienia się sezonowo [H01].
- Towar przychodzi w dostawach od dostawców: data przyjęcia, wiele pozycji (produkt + ilość) [H01].
- Płatność na miejscu, poza systemem; bez dowozu do domu [N19 §1, H01].
- Stan przed wdrożeniem: sklep nie ma systemu; stany prowadzone „z pamięci albo kartek” [H01 § SWOT/Szanse — sformułowanie zespołu, do potwierdzenia]. Obecny sposób przyjmowania rezerwacji (telefon, brak) ⛔.
- Problemy: straty z psucia się świeżego towaru [N19 §1]; brak możliwości wcześniejszej rezerwacji konkretnej ilości (np. 100 kg ziemniaków) [N19 §1]; niepewny stan rzeczywisty towaru [H01 § CSF]. Pozostałe problemy ⛔.
- Cel systemu: ograniczyć straty, pozwalając klientom rezerwować towar z wyprzedzeniem i odbierać go osobiście [N19 §1].
- Miejsce działania: fizyczny komputer w sklepie, bez zewnętrznego hostingu [N19 §1]. Sprzęt, system i sieć ⛔ (Q6).

### 6.2 Role

| Rola | Dostęp | Źródło |
|---|---|---|
| Klient-obserwator (gość) | przegląd asortymentu bez logowania; zakłada konto, gdy chce zarezerwować | [N19 uwaga 2] |
| Klient (zalogowany) | rezerwacja ilości, odbiór osobisty, płatność na miejscu; panel klienta | [N19 §1, uwaga 3] |
| Sprzedawca | Django Admin; dostawy, sprzedaż, obsługa rezerwacji | [N19 uwaga 3]; zakres czynności [H01] + [ZAŁ.] |
| Właściciel | Django Admin; produkty, ceny, konta personelu | [N19 uwaga 3]; podział uprawnień właściciel/sprzedawca [ZAŁ.] |
| Dostawca | bez konta; dostaje zamówienie z planu dostawy, właściciel rejestruje dostawę | [N19 uwaga 2]; brak konta — uzupełnienie agenta w Q7 (04.11), do akceptacji |

Właściciel i sprzedawca mogą być jedną osobą; rozdziela się role, nie etaty [H01 § Interesariusze].

### 6.3 Moduły funkcjonalne

| Moduł | Zakres | Źródło |
|---|---|---|
| Oferta | publiczny katalog produktów z ceną i dostępnością | [N19 §1, uwaga 2] |
| Konta klientów | rejestracja (w chwili rezerwacji), logowanie, wylogowanie, „moje dane” | [N19 uwaga 2]; reguły haseł ⛔ |
| Rezerwacje | złożenie rezerwacji ilości, anulowanie, lista „moje rezerwacje”; po stronie personelu przygotowanie, wydanie, odbiór | [N19 §1]; stany i wygasanie [ZAŁ.] — Q7 |
| Magazyn | produkty, dostawcy, dostawy z pozycjami, stan | [H01] |
| Sprzedaż | sprzedaż przy ladzie z pozycjami, zmniejszenie stanu, bez przekroczenia stanu | [H01] |
| Administracja | konta personelu i uprawnienia (grupy Django) | [N19 uwaga 3] + [ZAŁ.] |
| Raporty | np. sprzedaż i rezerwacje w okresie | [ZAŁ.] kandydat na wersję rozszerzoną [wzór: SH 2.4, SZ 2.3] — Q8 |

### 6.4 Proponowany stack

| Element | Propozycja | Źródło / status |
|---|---|---|
| Język | Python 3.12 | komputer deweloperski: Python 3.12.3 (odczyt 03.11.2026); wersja w sklepie ⛔ |
| Framework | Django 5.2 LTS | Django [N19]; wybór linii LTS [ZAŁ.] — zweryfikować aktualny numer poprawki przy tworzeniu `requirements.txt` (Q10) |
| Szablony | system szablonów Django (oddzielenie HTML od logiki) | [W4 pkt 9] |
| Baza | SQLite (MySQL/MariaDB jako ścieżka rozwoju) | SQLite [N19]; MySQL zalecany [W4 pkt 7]; ostrzeżenie o współbieżności [N19 uwaga 1] — **Q3 rozstrzygnięte 04.11.2026: SQLite** (WAL, `IMMEDIATE`, timeout; MySQL/MariaDB jako ścieżka rozwoju) |
| Panel personelu | `django.contrib.admin` | [N19 uwaga 3] |
| Uwierzytelnianie | `django.contrib.auth` + grupy (Właściciel, Sprzedawca, Klient) | [ZAŁ.] |
| Serwer w sklepie | serwer WSGI (np. waitress lub gunicorn) zamiast `runserver` | [ZAŁ.] — zależy od systemu w sklepie (Q6) |
| Licencje | Python (PSF), Django (BSD), SQLite (domena publiczna), MySQL/MariaDB (GPL) — narzędzia 0 zł | obowiązek wpisania licencji i 0 zł [N19 uwaga 6]; nazwy licencji [ZAŁ.] — zweryfikować w dokumentacji przed wpisaniem do raportu |

### 6.5 Podział na aplikacje Django [ZAŁ. w całości]

| Aplikacja | Zawartość | Warstwa |
|---|---|---|
| `config/` (projekt) | `settings`, `urls`, `wsgi` | konfiguracja |
| `katalog` | Produkt (+ Kategoria, jeśli Karol zechce); widok publicznego katalogu | dane + prezentacja |
| `magazyn` | Dostawca, Dostawa, PozycjaDostawy; logika zwiększania stanu | dane + kontrola |
| `sprzedaz` | Sprzedaż, PozycjaSprzedaży; logika zmniejszania stanu | dane + kontrola |
| `rezerwacje` | Rezerwacja, PozycjaRezerwacji; widoki klienta; zmiana statusów | dane + kontrola + prezentacja |
| `konta` | rejestracja, logowanie, profil klienta | kontrola + prezentacja |
| `templates/`, `static/` | szablony panelu klienta | prezentacja |

Wariant prostszy [ZAŁ.]: jedna aplikacja `sklep` z modułami `models.py`, `views/`, `services.py`. Wybór razem z Q11 (nazewnictwo PL/EN).

### 6.6 Zarys modelu danych

| Encja | Atrybuty (szkic) | Źródło |
|---|---|---|
| Produkt | nazwa, jednostka (kg / szt.), cena, stan, aktywny | nazwa, jednostka, cena, stan [H01]; „aktywny” = wycofanie z oferty [H01 sezonowość → ZAŁ.] |
| Dostawca | nazwa, kontakt | dostawca [H01]; atrybuty [ZAŁ.] |
| Dostawa | dostawca (FK), data przyjęcia | [H01] |
| PozycjaDostawy | dostawa (FK), produkt (FK), ilość | [H01] |
| Sprzedaż | data, osoba z personelu (FK) | zdarzenie z pozycjami [H01]; FK personelu [ZAŁ.] |
| PozycjaSprzedaży | sprzedaż (FK), produkt (FK), ilość, cena w chwili sprzedaży | [H01] |
| Klient | `User` + profil (np. telefon) | konto przy rezerwacji [N19 uwaga 2]; pola [ZAŁ.] |
| Rezerwacja | klient (FK), data złożenia, termin odbioru, status | rezerwacja z odbiorem osobistym [N19 §1]; termin i status [ZAŁ.] — Q7 |
| PozycjaRezerwacji | rezerwacja (FK), produkt (FK), ilość | rezerwacja „konkretnych ilości” [N19 §1] |

Reguły: stan rośnie przez dostawę, maleje przez sprzedaż i nie schodzi poniżej zera [H01]. Rezerwacja na dzień D zmniejsza pulę „plan dostawy na D − zarezerwowane na D” [Q7, 04.11]; sposób liczenia stanu — Q11. Statusy rezerwacji: złożona → odebrana / anulowana / nieodebrana [Q7, 04.11; wzór: SH 5.7]. Model musi dodatkowo obejmować: plan dostawy (produkt, dzień, ilość), standardową dzienną ilość produktu, zaległość klienta z opłatami za nieodebranie i wpłatami, identyfikator karty od operatora płatności [Q7]. Model powstaje code-first z klas ORM i jest opisywany jako „model bazy danych” [N19 uwaga 6].

### 6.7 Panel klienta a panel administratora

| | Panel klienta (własne widoki i szablony) | Django Admin |
|---|---|---|
| Użytkownicy | klient-obserwator, klient | właściciel, sprzedawca [N19 uwaga 3] |
| Funkcje | katalog i dostępność; rejestracja, logowanie; złożenie i anulowanie rezerwacji; moje rezerwacje | produkty i ceny, dostawy, sprzedaż, rezerwacje (zmiana statusu, wydanie), konta personelu |
| Uzasadnienie | bezpieczeństwo i wygoda klientów [N19 uwaga 3] | gotowy CRUD; zapas, gdy własne formularze się opóźnią [H01 § Wykonalność] |
| Dostęp | logowanie tylko dla rezerwacji; przegląd bez konta [N19 uwaga 2] | tylko `is_staff` + grupy [ZAŁ.] |

### 6.8 Kolejność budowy aplikacji

Terminy laboratoriów [PLAN]: 17.11 projekt, 30.11 implementacja i wdrożenie, 14.12 prezentacja. Daty pośrednie [ZAŁ.].

1. **Do 10.11:** środowisko (venv, `requirements.txt` z wersjami), `startproject`, modele Produkt / Dostawca / Dostawa / Sprzedaż z pozycjami, migracje, rejestracja w adminie. To realizuje zalecenie, by równolegle przygotować prostą działającą wersję [N19 „Ustalenia”].
2. **10.11–17.11:** modele Rezerwacja i PozycjaRezerwacji, profil klienta, grupy ról; eksport diagramu klas i ERD z modeli oraz SQL z `sqlmigrate` dla rozdz. 2.6 [N19 uwaga 6].
3. **17.11–24.11:** panel klienta (katalog, rejestracja i logowanie, złożenie, anulowanie i lista rezerwacji); reguły stanu w `transaction.atomic`; obsługa statusów rezerwacji w adminie; testy `TestCase` reguł stanu i rezerwacji.
4. **24.11–30.11:** ustawienia wdrożeniowe (`DEBUG=False`, `ALLOWED_HOSTS`), instalacja na komputerze w sklepie wg instrukcji [N19 uwaga 6], dane początkowe (fixtures), kopia i odtworzenie bazy, zrzuty ekranu do podręcznika, checklista odbioru.
5. **30.11–14.12:** poprawki, funkcje wersji rozszerzonej, jeśli zostanie czas (Q8), dane pokazowe, próba prezentacji.

---

## 7. Kolejność omawiania etapu 1 z Karolem

Zasada (jak w SH): najpierw jak sklep działa dziś, potem dlaczego potrzebny jest system i co zmienia, potem cel, zakres, ocena i plan. Każdy punkt to jedna rozmowa, po której agent pisze tekst sekcji. Kolumna „Pytania” wskazuje, co trzeba ustalić w rozmowie (numery z §5 i z listy braków w `docs/indeks-zrodel.md`). Wymagania 2.3–2.4 omawia się na początku etapu 2 (notatka 19.10, „Ustalenia”).

| Kolejność | Sekcja w `sprawozdanie.tex` | Pytania do ustalenia | Dlaczego w tym miejscu |
|---|---|---|---|
| 1 ✅ | 1.1 Obecny sposób działania sklepu + 1.3 Proponowany system + 1.5 Parametry skalowalne — **napisane 04.11.2026** (dawny „Opis słowny” podzielony 04.11 na „jak jest” i „co system wprowadza”); uzupełnienia agenta czekają na akceptację Karola | — (Q7 rozstrzygnięte) | Z opisu wynikają wszystkie kolejne sekcje etapu 1 i wymagania etapu 2 |
| 2 ✅ | 1.2 Problemy prowadzenia sklepu bez systemu — **napisane 04.11.2026** (P1–P8, etykiety `prob:rezerwacja`, `prob:zamawianie`, `prob:straty`, `prob:ewidencja`, `prob:informacja`, `prob:kolejki`, `prob:dostawa`, `prob:wiedza`; numeracja stała); uzupełnienia agenta do akceptacji Karola | — | Wynika z opisu „jak jest”; uzasadnia system i cel |
| 3 ✅ | 1.4 Interesariusze i otoczenie systemu — **napisane 04.11.2026** (`sec:otoczenie`, `tab:otoczenie`): zapłata za towar, kasa fiskalna i terminal poza systemem; dostawca bez konta; operator płatności tylko dla opłaty za nieodebranie; uzupełnienia agenta (pkt 30–33 w `CLAUDE.md`) do akceptacji | — | Domyka granicę systemu opisanego w 1.3 |
| 4 **następny** | 2.1 Cel projektu + 2.2 Zakres projektu (z „Uwagą”); przy okazji ustala się podział na wersje 2.5 | podział funkcji na wersje (Q8) | Cel odpowiada na P1–P8; zakres wynika z Q1 |
| 5 | 3.1 Analiza SWOT | punkty zespołu po poprawkach prowadzącego (N19 uwaga 5) | Wymaga znanego zakresu i ograniczeń |
| 6 | 3.2 Czynniki krytyczne sukcesu (CSF) | które warunki są sprawdzalne na działającej aplikacji | Wynikają z celu i ze SWOT |
| 7 | 3.3 Techniczna wykonalność systemu (3.3.1 technologie, wersje i licencje; 3.3.2 współbieżne zapisy w SQLite) | wersje (Q10), komputer w sklepie i dostęp klientów (Q6) | Najwięcej otwartych decyzji technicznych; potrzebny gotowy zakres |
| 8 | 3.4 Koszt wytworzenia systemu (kosztorys) | godziny i stawka albo szacunek względny, sprzęt (Q9) | Zależy od stosu i licencji z punktu 7 |
| 9 | 3.5 Plan projektu | czy daty pośrednie z §6.8 zostają | Plan zależy od zakresu |
| 10 | 3.6 Grupa projektowa i podział obowiązków (3.6.1 skład, 3.6.2 podział w etapach; tuż przed harmonogramem) | kto grał właściciela w wywiadzie; podział zadań i przebudowa `PLAN.md` (Q12) | Podział zależy od planu |
| 11 | 3.7 Harmonogram | daty etapów i rezultaty | Ostatnia sekcja części analitycznej; terminy znane |
| 12 | Specyfikacja projektu (bez numeru) | wersje technologii (Q10), baza (Q3) | Streszczenie całości — pisać na końcu (TODO w `.tex`) |
