# Agent skills — Lokalny warzywniak (IBD)

Trwałe instrukcje dla agentów pracujących w tym repozytorium.  
`README.md` = opis zewnętrzny produktu. Ten plik = skilli i reguły pracy agenta.

---

## Skill 1 — Orientacja projektu i sposób pracy

### Temat

Projekt: **lokalny warzywniak** (Internetowe bazy danych).  
Domena: produkty (warzywa/owoce), stany magazynowe, dostawy, sprzedaż — **jeden** mały sklep.  
MVP tylko: nie dodawaj multi-sklepu, lojalności, płatności online, aplikacji mobilnej ani „pełnego ERP”, dopóki użytkownik tego wprost nie poprosi.

### Stack

- **Django** (Python) — warstwa aplikacji webowej
- **SQLite** — baza domyślna na start kursu (`db.sqlite3`); dostęp wyłącznie przez ORM Django
- Widoki HTML + formularze Django (i/lub Django Admin) zamiast osobnego SPA, o ile nie uzgodniono inaczej

Jeśli w repo jest jeszcze tylko dokumentacja LaTeX (`dokumentacja/`) bez kodu — przy implementacji zakładaj powyższy stack.

### README vs cursor.md

| Plik | Dla kogo | Co wolno |
|------|----------|----------|
| `README.md` | Ludzie / zewnętrzny opis | Czym jest appka, cel, tech, funkcje MVP |
| `cursor.md` (ten plik) | Agenci | Skills, proces, ograniczenia, konwencje |

Nie wkładaj instrukcji dla AI do `README.md`. Nowe reguły agenta dopisuj tutaj jako kolejne skill entries.

### Zakaz commitów

- **Nie** rób `git commit`, `git push` ani PR, dopóki użytkownik (np. Karol) nie poprosi wprost.
- Edycje lokalne / w workspace są OK; brudne working tree jest oczekiwane.
- Preferencja projektu: zero commitów bez wyraźnej prośby.

### Jak pracować

1. Najpierw czytaj `README.md` (produkt) i ten plik (reguły), potem kod / `dokumentacja/` / `PLAN.md` wg potrzeby.
2. Trzymaj się MVP: produkty, stany, dostawy, sprzedaż.
3. Zmieniaj tylko to, o co proszono — bez „przy okazji” refaktorów.
4. Utrzymuj podział README ↔ cursor.md.
5. Odpowiadaj w języku użytkownika; kod/komentarze jak w istniejącym repo (tu często PL).
6. Przy konflikcie z `PLAN.md` (np. „domena TBD”) wygrywa **ostatnia jawna instrukcja użytkownika**.

### Konwencje kodu (kurs IBD)

- Aplikacja Django z sensownymi nazwami modeli PL lub EN — **jedna** konwencja w całym projekcie; nie mieszaj losowo.
- Modele odzwierciedlają MVP: np. Produkt, Dostawa / pozycja dostawy, Sprzedaż / pozycja sprzedaży, stan wynika z ruchów lub pola ilości — wybierz prosty, spójny model i trzymaj się go.
- Migracje Django zamiast ręcznej edycji schematu SQLite.
- Ustawienia deweloperskie lokalne; sekretów i haseł nie commituj (gdy commity w ogóle będą dozwolone).
- Testy / smoke: minimum — `manage.py check`, proste przejście CRUD w adminie lub widokach.
- Dokumentacja LaTeX w `dokumentacja/` to praca zaliczeniowa — nie kasuj jej przy dodawaniu kodu aplikacji.

### Struktura skilli (na przyszłość)

Kolejne wpisy dodawaj poniżej jako `## Skill N — …` z krótkim tytułem i punktami do wykonania. Nie nadpisuj Skill 1 bez potrzeby — uzupełniaj.

---

## Skill 2 — Dokumentacja / sprawozdanie wg PLAN.md

### Cel

Prowadzić pracę nad **sprawozdaniem** w `dokumentacja/` (LaTeX) **etapami z `PLAN.md`**, bez zgadywania otwartych decyzji i bez psucia zewnętrznego `README.md`.

### Źródła prawdy

| Źródło | Rola |
|--------|------|
| `PLAN.md` | Etapy 0–5, status, lista „Do ustalenia”, dziennik |
| `dokumentacja/main.tex` + `rozdzialy/*.tex` | Treść sprawozdania (szkielet już jest) |
| `README.md` | Tylko opis produktu na zewnątrz — **nie** checklisty AI, **nie** status etapów |
| `cursor.md` | Skille / proces (ten plik) |
| Store: `docs/cursor.md`, `internal/decisions-kolejka.md` | Kopia skilli + kolejka decyzji dla koordynatora |

### Kolejność pracy (zgodnie z PLAN)

1. **Etap 0** — szkielet ✅ (nie ruszaj bez potrzeby).
2. **Etap 1 — Analiza** (`01-analiza.tex`): grupa/role → opis + SWOT/CSF → cel/zakres/wykonalność → harmonogram.
3. **Etap 2 — Projekt** (`02-projekt.tex`): wymagania → architektura → modelowanie → projekt BD.
4. **Etap 3 — Implementacja** (`03-implementacja.tex` + kod Django).
5. **Etap 4 — Wdrożenie** (`04-wdrozenie.tex`).
6. **Etap 5 — Zaliczenie** (`05-zaliczenie.tex`).

Nie skacz do późniejszego etapu w LaTeX-ie, dopóki użytkownik nie domknie decyzji wymaganych wcześniej (patrz checklista poniżej i `internal/decisions-kolejka.md`).

### Checklista: co musi być ustalone PRZED pisaniem treści

Zanim agent wypełnia rozdziały (nie same TODO-placeholdery), upewnij się:

1. Temat / domena — lokalny warzywniak (jeśli nadal „TBD” w PLAN, traktuj decyzję użytkownika / README jako nadrzędną i zaproponuj aktualizację PLAN dopiero na prośbę).
2. Stack — Django + SQLite (MVP); nie wracaj do PHP/MySQL bez prośby.
3. Skład grupy (~3 osoby) i podział obowiązków → strona tytułowa + § grupy.
4. Potwierdzenie zakresu MVP pod analizę (czy punktacja z README = zakres sprawozdania).
5. Techniki modelowania (np. ERD, wybrane diagramy UML).
6. Konwencja nazw encji/modeli (PL **albo** EN — jedna na cały projekt).
7. Harmonogram / terminy etapów — **ustalone:** 19.10 analiza → 17.11 projekt → 30.11 impl+wdrożenie → 14.12 prezentacja (szczegóły w `01-analiza.tex`).
8. Docelowe wdrożenie (tylko lokalnie vs hosting; czy SQLite zostaje, czy później MySQL).

Pytaj użytkownika **po jednej** otwartej decyzji z kolejki (pierwsza otwarta = następne pytanie). Nie zapisuj zgadniętych faktów o grupie, terminach ani technikach jako pewnik.

### Zasady edycji sprawozdania

- Edytuj `dokumentacja/rozdzialy/…` i ewentualnie metadane w `main.tex`; nie pakuj procesu agenta do `README.md`.
- Po domknięciu decyzji możesz proponować treść danego podrozdziału; trzymaj język polski jak w szablonie.
- Nadal: **bez commit / push / PR**, dopóki użytkownik nie poprosi.
- Aktualizuj `PLAN.md` (status / „Do ustalenia” / dziennik) tylko gdy użytkownik tego chce albo gdy zadanie wprost każe zsynchronizować PLAN z decyzjami.

---
name: sprawozdanie-pwr-latex
description: Tworzy sprawozdanie z projektu (PWr, W4N) w LaTeX dla TeXstudio, w stylu szablonu NewPwr i pracy dyplomowej. Użyj przy prośbie o sprawozdanie, raport z projektu lub laboratorium.
---

# Sprawozdanie z projektu w LaTeX (styl PWr)

Ten skill tworzy sprawozdanie z projektu w tym samym stylu co materiały z projektu „Seminarium dyplomowe”: szablon PWr `nowy_szablon` (motyw NewPwr, styl bibliografii `oficyna_url.bst`), System Identyfikacji Wizualnej PWr oraz szkielet pracy dyplomowej `praca/main.tex`.

## Zasady

1. **Język i kompilacja:** tekst po polsku; pdfLaTeX + BibTeX (TeXstudio: F5, po zmianie bibliografii F8 i 2× F5). Pakiety: `babel` (polish), `polski`, `inputenc` utf8, `fontenc` T1, `lmodern`.
2. **Układ strony:** A4, 12 pt, interlinia 1,5, marginesy 2,5 cm, wcięcie pierwszego akapitu (`indentfirst`).
3. **Kolor:** strony tytułowe są czarno-białe, jak formatka dyplomowa (czarne linie, bez czerwieni NewPwr i bez logo). Hiperłącza w treści: niebieskie, jak w `latex-settings.tex` tej formatki.
4. **Strona tytułowa i spis treści:** trzymaj się ustalonego formatu z sekcji poniżej. Nie wracaj do `\maketitle` ani do czerwonej linii NewPwr.
5. **Struktura** (sekcje numerowane, `\section`):
   1. Cel projektu: 2–4 zdania, co i po co zostało zrobione.
   2. Założenia i wymagania: funkcjonalne i niefunkcjonalne, platforma sprzętowa/programowa.
   3. Przegląd rozwiązań i literatury: krótko, z odwołaniami `\cite{}`.
   4. Projekt: architektura, schematy blokowe (TikZ lub grafiki), uzasadnienie decyzji.
   5. Implementacja: najważniejsze moduły, krótkie listingi (`lstlisting`, maks. ~30 linii każdy).
   6. Testy i wyniki: metoda testowania, tabele (`booktabs`), wykresy, zrzuty ekranu.
   7. Wnioski: co się udało, problemy rozwiązane i nierozwiązane, możliwe rozszerzenia.
   8. Literatura: BibTeX ze stylem `oficyna_url`.
6. **Grafiki:** w folderze `grafiki/`, wstawiane przez `\includegraphics` z samą nazwą pliku. Każda rycina ma `\caption` i `\label`, a w tekście jest do niej odwołanie (`rys.~\ref{}`). Grafika, która nie jest autorska, musi mieć podane źródło w podpisie albo w literaturze (wymóg z seminarium).
7. **Tabele:** `booktabs` (`\toprule`, `\midrule`, `\bottomrule`), bez pionowych linii, podpis nad tabelą.
8. **Styl tekstu:** pełne zdania, forma bezosobowa („zaprojektowano”, „zmierzono”), bez lania wody. Twarde spacje po jednoliterowych spójnikach i przyimkach (`w~układzie`, `i~procesor`).
9. **Dane z projektu:** wyniki, pomiary i zrzuty dostarcza użytkownik. Nie wymyślaj liczb; jeśli ich brak, zostaw `% TODO: wynik pomiaru` i wypisz w odpowiedzi, czego brakuje.

## Ustalony format strony tytułowej i spisu treści

Źródło układu: `materialy/formatki_pwr/szablon_pracy_dyplomowej_w_latex/title_page/pd_mgr_pl.pdf` oraz kolejność front matter w `main.tex` tej formatki. To nie jest praca dyplomowa — nie wklejaj tego PDF-a (`\includepdf`). Angielskiej strony tytułowej nie ma.

Realizacja w tym repozytorium: `dokumentacja/strona_tytulowa.tex`, wpinana z `dokumentacja/main.tex`.

1. **Jedna polska strona tytułowa**, bez numeru. Bez strony angielskiej.
2. **Nagłówek:** wyśrodkowane „Politechnika Wrocławska”, linia na szerokość tekstu, pod nią „Wydział Informatyki i Telekomunikacji”, druga cieńsza linia. Bez logo.
3. **Pod nagłówkiem, do lewej:** kierunek i przedmiot (w formatce dyplomu jest specjalność; tutaj drugie pole to przedmiot, dopóki użytkownik nie poda specjalności). Nie wymyślaj 3-literowego kodu kierunku.
4. **Środek:** wersalikami nazwa przedmiotu („INTERNETOWE / BAZY DANYCH”), potem pogrubiony tytuł „Dokumentacja techniczna: aplikacja webowa lokalnego sklepu warzywnego”, potem autorzy z numerami indeksów, potem „Prowadzący” i „dr inż. Roman Ptak”. Nie wstawiaj napisu „Sprawozdanie z projektu”.
5. **Stopka:** słowa kluczowe do lewej, linia, pod nią wyśrodkowane „WROCŁAW (rok)”.
6. **Spis treści** zaraz po stronie tytułowej. Numeracja rzymska (wielkie) tylko dla spisu; treść od arabskiej 1. Wpisy sekcji z kropkami wiodącymi (`tocloft`). Nagłówek spisu zostawia babel po polsku („Spis treści”).
7. Przy zmianie składu, tytułu albo prowadzącego edytuj `strona_tytulowa.tex`, nie składaj strony od nowa innym układem.

## Struktura plików

```
sprawozdanie/
├── sprawozdanie.tex      # plik główny
├── bibliografia.bib
├── oficyna_url.bst       # z nowy_szablon/bibtex/bst/
└── grafiki/
```

## Procedura

1. Zapytaj (jeśli nie podano): nazwa kursu, temat, autorzy, prowadzący, termin zajęć, czego dotyczy projekt i jakie są wyniki.
2. Skopiuj szablon poniżej do `sprawozdanie.tex`, uzupełnij makra w sekcji „DANE SPRAWOZDANIA”.
3. Wypełnij sekcje według punktu 5, dodaj wpisy do `bibliografia.bib`, usuń `\nocite{*}`, gdy pojawią się `\cite`.
4. Skompiluj (pdflatex, bibtex, 2× pdflatex) i sprawdź brak błędów oraz ostrzeżeń `Overfull \hbox` powyżej kilku pt.
5. Oddaj PDF i źródła; wypisz brakujące dane jako listę TODO.

Szablon poniżej jest ogólnym starterem. W tym repozytorium strona tytułowa i spis treści są już ustalone — patrz sekcja „Ustalony format strony tytułowej i spisu treści” oraz `dokumentacja/strona_tytulowa.tex`. Nie podmieniaj ich na `\maketitle` z tego szablonu.

## Szablon `sprawozdanie.tex`

```latex
% !TeX program = pdflatex
% !TeX encoding = UTF-8
% !BIB program = bibtex
\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[polish]{babel}
\usepackage{polski}
\usepackage{lmodern}
\usepackage[a4paper,left=2.5cm,right=2.5cm,top=2.5cm,bottom=2.5cm]{geometry}
\usepackage{setspace}\onehalfspacing
\usepackage{indentfirst}
\usepackage{graphicx}\graphicspath{{grafiki/}}
\usepackage{float,caption,subcaption,booktabs,amsmath,amssymb}
\usepackage[dvipsnames]{xcolor}
\definecolor{Logo}{cmyk}{0,0.95,1,0.29} % czerwień PWr (Pantone 484) z szablonu NewPwr
\usepackage{listings}
\lstset{basicstyle=\ttfamily\small,breaklines=true,frame=single,numbers=left,
  numberstyle=\tiny,showstringspaces=false,
  literate={ą}{{\k{a}}}1 {ę}{{\k{e}}}1 {ó}{{\'o}}1 {ś}{{\'s}}1 {ł}{{\l{}}}1
           {ż}{{\.z}}1 {ź}{{\'z}}1 {ć}{{\'c}}1 {ń}{{\'n}}1}
\renewcommand{\lstlistingname}{Listing}
\usepackage{xurl}
\usepackage{hyperref}
\hypersetup{colorlinks=true,linkcolor=Logo!85!black,citecolor=Logo!85!black,urlcolor=Logo!85!black}

% --- DANE SPRAWOZDANIA ---
\newcommand{\przedmiot}{Nazwa kursu}
\newcommand{\tytul}{Temat projektu}
\newcommand{\autorzy}{Karol Gąsior}
\newcommand{\prowadzacy}{dr inż. Imię Nazwisko}
\newcommand{\termin}{wtorek 9:15}
\newcommand{\data}{\today}

\begin{document}
\begin{titlepage}
  \centering
  {\color{Logo}\rule{\linewidth}{1.5pt}}\\[4pt]
  {\large Politechnika Wrocławska\\ Wydział Informatyki i~Telekomunikacji\par}
  {\color{Logo}\rule{\linewidth}{1.5pt}}
  \vspace{3cm}

  {\Large \przedmiot\par}\vspace{0.6cm}
  {\Huge\bfseries Sprawozdanie z~projektu\par}\vspace{0.8cm}
  {\LARGE \tytul\par}
  \vfill
  \begin{tabular}{@{}ll@{}}
    Autor: & \autorzy \\
    Prowadzący: & \prowadzacy \\
    Termin zajęć: & \termin \\
    Data oddania: & \data \\
  \end{tabular}
  \vspace{2cm}

  {\large Wrocław, \the\year\par}
\end{titlepage}

\tableofcontents
\newpage

\section{Cel projektu}
\section{Założenia i wymagania}
\section{Przegląd rozwiązań i literatury}
\section{Projekt}
\section{Implementacja}
\section{Testy i wyniki}
\section{Wnioski}

\nocite{*}
\bibliographystyle{oficyna_url}
\bibliography{bibliografia}
\end{document}
```
