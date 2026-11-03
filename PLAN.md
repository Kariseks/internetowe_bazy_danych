# PLAN — kolejka obowiązków do TeXa

Krótki prompt wystarczy. Agent bierze stąd jeden obowiązek, wpisuje go do wskazanego miejsca i oznacza status.

## Jak pisać

| Prompt | Co robi agent |
|--------|----------------|
| `następny` | Pierwszy wiersz ze statusem ⬜ |
| `1.2` | Tylko obowiązek o tym numerze |
| `status` | Mówi, co jest następne. Nic nie edytuje |

Jeden prompt = jeden obowiązek. Bez commita, dopóki nie padnie osobna prośba.

**Następny:** `następny` → **1.2** Problemy prowadzenia sklepu bez systemu. Punkty 1.3–1.8 są już wpisane; 1.9 i 1.10 czekają na przydział osoby.

## Ustalenia (nie pytaj od nowa)

- Domena: jeden lokalny sklep warzywny. MVP: asortyment, stany, dostawy, sprzedaż. Bez wielu sklepów, płatności online, lojalności i aplikacji mobilnej.
- Stack: Django + SQLite. Płatność poza systemem.
- Grupa: Karol Gąsior 280913, Mikołaj Winiecki 280952, Mateusz Złośnik 281201. Prowadzący: dr inż. Roman Ptak.
- Terminy: 19.10 analiza, 17.11 projekt, 30.11 implementacja i wdrożenie, 14.12 prezentacja. Szczegóły w `01-analiza.tex`.
- Styl TeXa: polski, forma bezosobowa, twarde spacje po `a i o u w z`, bez wymyślonych cen i pomiarów.

## Kolejka

Status: ⬜ do zrobienia, ✅ wpisane.

### Etap 1 — `dokumentacja/rozdzialy/01-analiza.tex`

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
| 1.9 | Koszt wytworzenia: praca zespołu, sprzęt, licencje, hosting (wytyczne 4d) | do ustalenia | `\subsection{Wykonalność}` — nowy akapit i tabela kosztu | ⬜ |
| 1.10 | Plan projektu na poziomie ogólnym: kolejność prac i zależności etapów (wytyczne 4c) | do ustalenia | `\subsection{Plan projektu i harmonogram}` — tekst przed tabelą | ⬜ |

### Etap 2 — `dokumentacja/rozdzialy/02-projekt.tex`

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
| 2.9 | Diagram aktywności albo sekwencji: sprzedaż ze zmianą stanu (wytyczne 5: struktura funkcjonalna) | do ustalenia | `\subsection{Modelowanie}` — zachowanie | ⬜ |

W 2.3 opisz też szablony Django jako warstwę prezentacji (wytyczne 9) i uzasadnij SQLite zamiast zalecanego MySQL (wytyczne 7–8).

Diagramy 2.4–2.6 i 2.9: jeśli nie ma pliku w `dokumentacja/figury/`, opisz rysunek słownie i zostaw `% TODO: rysunek`. Nie wymyślaj grafiki.

### Etap 3 — `dokumentacja/rozdzialy/03-implementacja.tex` (+ kod, gdy dojdzie kolej)

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

### Etap 4 — `dokumentacja/rozdzialy/04-wdrozenie.tex`

| ID | Obowiązek | Kto | Miejsce | Status |
|----|-----------|-----|---------|--------|
| 4.1 | Plik zależności i środowisko wirtualne | Mateusz Złośnik | nowa podsekcja środowiska | ⬜ |
| 4.2 | Instrukcja uruchomienia na komputerze lokalnym | Karol Gąsior | nowa podsekcja instrukcji | ⬜ |
| 4.3 | Dane początkowe asortymentu i stanów | Mikołaj Winiecki | nowa podsekcja danych | ⬜ |
| 4.4 | Konta do pracy codziennej i do pokazu | Mateusz Złośnik | ta sama podsekcja albo osobna | ⬜ |
| 4.5 | Kopia zapasowa bazy SQLite i jej odtworzenie | Karol Gąsior | nowa podsekcja kopii | ⬜ |
| 4.6 | Checklista odbioru po wdrożeniu | Mikołaj Winiecki | nowa podsekcja odbioru | ⬜ |

### Etap 5 — `dokumentacja/rozdzialy/05-ocena_efektow.tex`

| ID | Obowiązek | Kto | Miejsce | Status |
|----|-----------|-----|---------|--------|
| 5.1 | Scenariusz prezentacji i podział wypowiedzi | Mateusz Złośnik | nowa podsekcja scenariusza | ⬜ |
| 5.2 | Dane pokazowe w działającym sklepie | Karol Gąsior | nowa podsekcja danych pokazowych | ⬜ |
| 5.3 | Demonstracja funkcji MVP | Mikołaj Winiecki | ta sama podsekcja albo osobna | ⬜ |
| 5.4 | Konspekt albo slajdy | Mateusz Złośnik | nowa podsekcja konspektu | ⬜ |
| 5.5 | Próba generalna i pomiar czasu | Karol Gąsior | dopisz do konspektu albo osobna podsekcja; czas tylko jeśli podany | ⬜ |
| 5.6 | Wnioski w dokumentacji i oddanie PDF | Mikołaj Winiecki | nowa podsekcja wniosków | ⬜ |

Obowiązki ogólne z tabeli (repozytorium, skład PDF, terminy, przegląd kodu) nie są osobnymi podrozdziałami. Nie wstawiaj ich do TeXa.

Nowe obowiązki 1.9, 1.10 i 2.9 trzeba też dopisać do tabeli `tab:obowiazki` w `01-analiza.tex`, gdy grupa przydzieli osoby.

## Plan całego sprawozdania wg wytycznych v4

Skill: `.cursor/skills/sprawozdanie-ibd/SKILL.md` (tabela wytyczne → rozdział, reguły treści, kontrola przed oddaniem).

| Termin | Etap | Rozdział | Do zrobienia | Zależy od |
|--------|------|----------|--------------|-----------|
| 19.10 (zaległe) | 1. Analiza | `01-analiza.tex` | 1.2, 1.9, 1.10 | — |
| 17.11 | 2. Projekt | `02-projekt.tex` | 2.1–2.2 wymagania → 2.3 architektura → 2.6 ERD → 2.7–2.8 baza → 2.4, 2.5, 2.9 diagramy | wymagania przed diagramami; ERD przed słownikiem |
| 30.11 | 3. Implementacja i walidacja | `03-implementacja.tex` + kod | 3.1 szkielet → 3.2–3.5 modele i migracje → 3.6–3.8 widoki, szablony, admin → 3.9 testy | modele zgodne z ERD z 2.6 |
| 30.11 | 4. Wdrożenie | `04-wdrozenie.tex` | 4.1 środowisko → 4.2 instrukcja → 4.3–4.4 dane i konta → 4.5 kopia → 4.6 odbiór | działająca ścieżka z 3.7 |
| 14.12 | 5. Prezentacja | `05-ocena_efektow.tex` | 5.1–5.5 pokaz, 5.6 wnioski i PDF | wdrożenie z 4.6 |

Kolejność w etapie 2 nie jest kolejnością tabeli: najpierw wymagania i ERD, bo od nich zależą diagramy, słownik i modele Django z etapu 3.

### Część Karola Gąsiora

| ID | Co | Jak zrealizować | Czeka na |
|----|----|-----------------|----------|
| 2.3 | Architektura | Rysunek trzech warstw (przeglądarka + szablony, widoki i formularze, ORM + SQLite), tabela warstwa → katalog Django, akapit o szablonach jako odpowiedniku Smarty, uzasadnienie SQLite i ścieżka do MySQL | — |
| 2.6 | ERD | Encje Produkt, StanMagazynowy (albo pole stanu w Produkcie — decyzja), Dostawca, Dostawa, PozycjaDostawy, Sprzedaż, PozycjaSprzedaży; liczności związków; plik w `figury/` | decyzja o stanie |
| 3.2 | Model produktu i stanu | Modele zgodne z ERD, ograniczenie stanu ≥ 0, krótki listing | 2.6, 3.1 |
| 3.4 | Model sprzedaży | Sprzedaż i pozycja z ceną z chwili sprzedaży | 3.2 |
| 3.7 | Widoki dostaw i sprzedaży | Formularz z pozycjami, zmiana stanu w jednej transakcji (`transaction.atomic`), odmowa sprzedaży ponad stan | 3.3, 3.4 |
| 4.2 | Instrukcja uruchomienia | Kroki od klonowania do `runserver`, sprawdzone na czystym środowisku | 4.1 |
| 4.5 | Kopia bazy | Kopia pliku `db.sqlite3` albo `dumpdata`/`loaddata`, sprawdzone odtworzenie | 4.3 |
| 5.2 | Dane pokazowe | Fixture z kilkoma produktami, dostawą i sprzedażą | 4.3 |
| 5.5 | Próba generalna | Przejście scenariusza 5.1, czas tylko zmierzony | 5.1, 5.3 |

### Otwarte pytania

1. Foldery z przykładami (IO, bazy danych) nie są w repozytorium — trzeba je dodać i wypchnąć, wtedy skill dostanie sekcję wzorców.
2. Koszt wytworzenia (1.9): liczymy godziny × stawkę (jakie wartości?) czy tylko koszty zerowe licencji i sprzętu plus godziny?
3. SQLite zostaje z uzasadnieniem czy przechodzimy na zalecany MySQL?
4. Stan magazynowy: osobna encja czy pole w produkcie?
5. Kto bierze 1.9, 1.10 i 2.9?
6. Narzędzie do diagramów: draw.io, PlantUML czy TikZ?

## Dziennik

- **2026-10-19** — szkielet projektu i dokumentacji LaTeX.
- **2026-10-19** — skład grupy, uczelnia, wydział, kierunek, prowadzący, podział obowiązków.
- **2026-10-19** — kolejka obowiązków do krótkich promptów. Wpisano 1.1 (opis słowny sklepu). 1.8 było już w harmonogramie.
- **2026-10-19** — wpisano 1.3–1.7. Został 1.2. Szacunek pracochłonności jest względny, bez godzin.
- **2026-11-03** — skill `sprawozdanie-ibd` zgodny z wytycznymi v4. Dodano 1.9 (koszt), 1.10 (plan ogólny), 2.9 (diagram zachowania), plan całości i otwarte pytania.
