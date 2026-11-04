# PLAN — kolejka obowiązków do TeXa

> **Nieaktualne od 03.11.2026.** Kolejka powstała przed decyzjami Q1 (rezerwacje klientów w MVP) i Q2 (etap 1 pisany od nowa), więc statusy ✅ etapu 1 i linijka „Następny” nie obowiązują. Aktualny plan i kolejność pracy: `docs/plan-sprawozdania.md` (§7 — kolejność omawiania etapu 1), instrukcje: `CLAUDE.md`. Przebudowa tej kolejki czeka na decyzję Q12.

Krótki prompt wystarczy. Agent bierze stąd jeden obowiązek, wpisuje go do wskazanego miejsca i oznacza status.

## Jak pisać

| Prompt | Co robi agent |
|--------|----------------|
| `następny` | Pierwszy wiersz ze statusem ⬜ |
| `1.2` | Tylko obowiązek o tym numerze |
| `status` | Mówi, co jest następne. Nic nie edytuje |

Jeden prompt = jeden obowiązek. Bez commita, dopóki nie padnie osobna prośba.

**Następny:** `następny` → **1.2** Problemy prowadzenia sklepu bez systemu. Punkty 1.3–1.7 są już wpisane.

## Ustalenia (nie pytaj od nowa)

- Domena: jeden lokalny sklep warzywny. MVP: asortyment, stany, dostawy, sprzedaż. Bez wielu sklepów, płatności online, lojalności i aplikacji mobilnej.
- Stack: Django + SQLite. Płatność poza systemem.
- Grupa: Karol Gąsior 280913, Mikołaj Winiecki 280952, Mateusz Złośnik 281201. Prowadzący: dr inż. Roman Ptak.
- Terminy: 19.10 analiza, 17.11 projekt, 30.11 implementacja i wdrożenie, 14.12 prezentacja. Szczegóły w `dokumentacja/sprawozdanie.tex` (§ Harmonogram).
- Styl TeXa: polski, forma bezosobowa, twarde spacje po `a i o u w z`, bez wymyślonych cen i pomiarów.

## Kolejka

Status: ⬜ do zrobienia, ✅ wpisane.

### Etap 1 — `dokumentacja/sprawozdanie.tex` (sekcja 1)

| ID | Obowiązek | Kto | Miejsce | Status |
|----|-----------|-----|---------|--------|
| 1.1 | Opis słowny sklepu: asortyment, dostawy, sprzedaż i stany | Karol Gąsior | `\subsection{Opis słowny sklepu}` | ✅ |
| 1.2 | Problemy prowadzenia sklepu bez systemu | Mateusz Złośnik | `\subsection{Problemy prowadzenia sklepu bez systemu}` | ⬜ |
| 1.3 | Interesariusze i otoczenie podsystemu | Mikołaj Winiecki | `\subsection{Interesariusze i otoczenie podsystemu}` | ✅ |
| 1.4 | Analiza SWOT | Karol Gąsior | `\subsection{Analiza SWOT}` | ✅ |
| 1.5 | Czynniki krytyczne sukcesu | Mateusz Złośnik | `\subsection{Czynniki krytyczne sukcesu}` | ✅ |
| 1.6 | Cel systemu i granice zakresu MVP | Mikołaj Winiecki | `\subsection{Cel systemu i zakres}` | ✅ |
| 1.7 | Wykonalność techniczna i szacunek pracochłonności | Karol Gąsior | `\subsection{Wykonalność}` | ✅ |
| 1.8 | Zgodność harmonogramu z terminami laboratorium | Mikołaj Winiecki | `\subsection{Plan projektu i harmonogram}` | ✅ |

### Etap 2 — `dokumentacja/sprawozdanie.tex` (sekcja 2)

| ID | Obowiązek | Kto | Miejsce | Status |
|----|-----------|-----|---------|--------|
| 2.1 | Wymagania funkcjonalne MVP | Mikołaj Winiecki | `\subsection{Wymagania funkcjonalne i niefunkcjonalne}` — tylko funkcjonalne | ⬜ |
| 2.2 | Wymagania niefunkcjonalne | Mateusz Złośnik | ta sama podsekcja — tylko niefunkcjonalne | ⬜ |
| 2.3 | Architektura trójwarstwowa: przeglądarka, Django, SQLite | Karol Gąsior | `\subsection{Architektura systemu}` | ⬜ |
| 2.4 | Diagram przypadków użycia | Mateusz Złośnik | `\subsection{Modelowanie}` — przypadki użycia | ⬜ |
| 2.5 | Diagram klas albo komponentów | Mikołaj Winiecki | `\subsection{Modelowanie}` — klasy lub komponenty | ⬜ |
| 2.6 | Diagram związków encji (ERD) | Karol Gąsior | `\subsection{Modelowanie}` — ERD | ⬜ |
| 2.7 | Klucze, związki i uzasadnienie postaci normalnej | Mikołaj Winiecki | `\subsection{Projekt bazy danych}` | ⬜ |
| 2.8 | Słownik danych: atrybuty, typy i ograniczenia | Mateusz Złośnik | `\subsection{Projekt bazy danych}` — słownik | ⬜ |

Diagramy 2.4–2.6: jeśli nie ma pliku w `dokumentacja/figury/`, opisz rysunek słownie i zostaw `% TODO: rysunek`. Nie wymyślaj grafiki.

### Etap 3 — `dokumentacja/sprawozdanie.tex` (sekcja 3) (+ kod, gdy dojdzie kolej)

| ID | Obowiązek | Kto | Miejsce | Status |
|----|-----------|-----|---------|--------|
| 3.1 | Szkielet projektu Django i aplikacji sklepu | Mateusz Złośnik | `\subsection{Struktura aplikacji}` | ⬜ |
| 3.2 | Model produktu i stanu magazynowego | Karol Gąsior | nowa podsekcja modeli | ⬜ |
| 3.3 | Model dostawy i pozycji dostawy | Mikołaj Winiecki | ta sama podsekcja | ⬜ |
| 3.4 | Model sprzedaży i pozycji sprzedaży | Karol Gąsior | ta sama podsekcja | ⬜ |
| 3.5 | Migracje schematu do SQLite | Mikołaj Winiecki | podsekcja modeli albo struktury | ⬜ |
| 3.6 | Widoki i formularze produktów | Mateusz Złośnik | nowa podsekcja widoków | ⬜ |
| 3.7 | Widoki i formularze dostaw oraz sprzedaży, ze zmianą stanu | Karol Gąsior | ta sama podsekcja | ⬜ |
| 3.8 | Konfiguracja panelu administratora | Mikołaj Winiecki | `\subsection{Struktura aplikacji}` albo osobna podsekcja | ⬜ |
| 3.9 | Test przejścia CRUD i opis wyników | Mateusz Złośnik | `\subsection{Walidacja i testy}` | ⬜ |

Kod Django powstaje razem z obowiązkiem, który go opisuje. `\subsection{Stack technologiczny}` uzupełnij przy 3.1 (Django, SQLite). Bez wyników testu zostaw `% TODO` w 3.9.

### Etap 4 — `dokumentacja/sprawozdanie.tex` (sekcja 4)

| ID | Obowiązek | Kto | Miejsce | Status |
|----|-----------|-----|---------|--------|
| 4.1 | Plik zależności i środowisko wirtualne | Mateusz Złośnik | nowa podsekcja środowiska | ⬜ |
| 4.2 | Instrukcja uruchomienia na komputerze lokalnym | Karol Gąsior | nowa podsekcja instrukcji | ⬜ |
| 4.3 | Dane początkowe asortymentu i stanów | Mikołaj Winiecki | nowa podsekcja danych | ⬜ |
| 4.4 | Konta do pracy codziennej i do pokazu | Mateusz Złośnik | ta sama podsekcja albo osobna | ⬜ |
| 4.5 | Kopia zapasowa bazy SQLite i jej odtworzenie | Karol Gąsior | nowa podsekcja kopii | ⬜ |
| 4.6 | Checklista odbioru po wdrożeniu | Mikołaj Winiecki | nowa podsekcja odbioru | ⬜ |

### Etap 5 — `dokumentacja/sprawozdanie.tex` (sekcja 5)

| ID | Obowiązek | Kto | Miejsce | Status |
|----|-----------|-----|---------|--------|
| 5.1 | Scenariusz prezentacji i podział wypowiedzi | Mateusz Złośnik | nowa podsekcja scenariusza | ⬜ |
| 5.2 | Dane pokazowe w działającym sklepie | Karol Gąsior | nowa podsekcja danych pokazowych | ⬜ |
| 5.3 | Demonstracja funkcji MVP | Mikołaj Winiecki | ta sama podsekcja albo osobna | ⬜ |
| 5.4 | Konspekt albo slajdy | Mateusz Złośnik | nowa podsekcja konspektu | ⬜ |
| 5.5 | Próba generalna i pomiar czasu | Karol Gąsior | dopisz do konspektu albo osobna podsekcja; czas tylko jeśli podany | ⬜ |
| 5.6 | Wnioski w dokumentacji i oddanie PDF | Mikołaj Winiecki | nowa podsekcja wniosków | ⬜ |

Obowiązki ogólne z tabeli (repozytorium, skład PDF, terminy, przegląd kodu) nie są osobnymi podrozdziałami. Nie wstawiaj ich do TeXa.

## Dziennik

- **2026-10-19** — szkielet projektu i dokumentacji LaTeX.
- **2026-10-19** — skład grupy, uczelnia, wydział, kierunek, prowadzący, podział obowiązków.
- **2026-10-19** — kolejka obowiązków do krótkich promptów. Wpisano 1.1 (opis słowny sklepu). 1.8 było już w harmonogramie.
- **2026-10-19** — wpisano 1.3–1.7. Został 1.2. Szacunek pracochłonności jest względny, bez godzin.
