---
name: styl-sprawozdania
description: Zasady stylu, jakości tekstu i składu LaTeX dla sprawozdania IBD (lokalny warzywniak). Użyj zawsze przed napisaniem lub poprawieniem jakiegokolwiek tekstu w dokumentacja/sprawozdanie.tex, także przy szkicach sekcji pokazywanych Karolowi.
---

# Styl i jakość tekstu sprawozdania IBD

Poziom docelowy: raport, który prowadzący oceni jako dobrą pracę studencką. Tekst ma być rzeczowy, sprawdzalny i osadzony w realiach jednego małego sklepu warzywnego. Fakty pochodzą wyłącznie ze źródeł (skill `zrodla-sprawozdania`) albo od Karola.

## Wzór tonu w materiałach

Przed pisaniem pierwszej sekcji danego typu przeczytaj wzorzec:

- **Sklep hydrauliczny, rozdz. 2.1 „Cel projektu”** (`materialy/bazdy danych/Sklep hydrauliczny - przykładowy raport.pdf`, s. 11). Trzy krótkie akapity: co system robi, dla kogo, w jakiej formie; na końcu „Uwaga:” z jawną listą tego, czego system nie robi. Żadnych przymiotników oceniających.
- **Sklep hydrauliczny, rozdz. 10 „Wnioski”** (ten sam plik, s. 99). Każdy wniosek nazywa konkretną rzecz (brak statystyk sprzedaży, brak wersji responsywnej, korekty modelu danych w trakcie implementacji) i jej skutek.
- Kontrprzykład: **Szkółka narciarska, rozdz. 8** (s. 65–66) zawiera zdania typu „Praca zespołowa znacząco zwiększa efektywność realizacji projektu” i „Szczegółowa dokumentacja projektu ułatwia jego realizację”. Takie zdania pasują do każdego projektu, więc nic nie mówią. Nie pisz w ten sposób.

## Rejestr

1. **Język:** polski, rejestr akademicko-techniczny.
2. **Osoba:** w projekcie wybrano formę bezosobową („zaprojektowano”, „przyjęto”, „system umożliwia”) i stosuje się ją w całym raporcie. Pierwszej osoby liczby mnogiej („zaprojektowaliśmy”) nie używa się; mieszanie obu form, nawet między rozdziałami, jest błędem.
3. **Czas:** przeszły dla wykonanych prac („przeprowadzono wywiad”), teraźniejszy dla opisu sklepu i systemu („sprzedawca przyjmuje dostawę”, „system blokuje zarezerwowaną ilość”).
4. **Terminy:** jedno słowo na jedno pojęcie w całym raporcie, zgodne z kodem i słownikiem danych. Ustalone: „rezerwacja”, „pozycja rezerwacji”, „produkt”, „dostawa”, „sprzedaż”, „stan” (nie zamiennie „zapas”, „ilość w magazynie”), „klient-obserwator”, „panel klienta”, „panel administratora (Django Admin)”. Nowy termin definiuje się przy pierwszym użyciu.
5. **Akapity:** jeden akapit = jedna myśl, zwykle 3–6 zdań. Pierwsze zdanie akapitu mówi, o czym on jest.
6. **Zakotwiczenie:** każde twierdzenie dotyczy warzywniaka albo ma źródło. Zamiast „system usprawnia obsługę klienta” — „klient rezerwuje 20~kg ziemniaków przez panel klienta, a~sprzedawca widzi rezerwację przed przyjęciem dostawy”. Ogólne prawdy o bazach danych czy frameworkach pomija się, chyba że uzasadniają decyzję projektową.
7. **Liczby zamiast ogólników:** „kilkadziesiąt produktów” → liczba od Karola; „szybko” → czas; „wielu użytkowników” → ilu naraz. Wartość z jednostką i twardą spacją: `100~kg`, `0~zł`, `2~tygodnie`. Brak liczby → `% TODO: <co, kto podaje>` i pytanie do Karola, nigdy liczba wymyślona.
8. **Zdania:** średnio 15–25 słów; zdanie dłuższe niż 35 słów dzieli się. Strona czynna, gdy znany jest wykonawca („sprzedawca zatwierdza rezerwację”), zamiast łańcuchów rzeczowników odczasownikowych („dokonanie zatwierdzenia rezerwacji”).

## Zakazane „AI-izmy”

Poniższe frazy i wzorce sygnalizują tekst wygenerowany i obniżają ocenę. Nie używaj ich; jeśli pojawią się w szkicu, przepisz zdanie.

**Frazy-wypełniacze**

| Zamiast | Pisz |
|---|---|
| „warto zauważyć, że”, „należy podkreślić, że”, „co istotne” | samo twierdzenie |
| „w dzisiejszych czasach”, „w dobie cyfryzacji”, „w erze” | nic albo konkretna data/fakt |
| „kluczowy”, „kluczowe znaczenie” jako ozdobnik | „konieczny”, „wymagany” albo nic; „kluczowy” tylko w sensie dosłownym (klucz główny) |
| „kompleksowy”, „innowacyjny”, „nowoczesny”, „zaawansowany”, „intuicyjny” | konkret: co system robi |
| „odgrywa istotną/kluczową rolę”, „stanowi istotny element” | co dokładnie robi i dla kogo |
| „szeroki wachlarz”, „szereg możliwości”, „wiele korzyści” | lista konkretnych funkcji |
| „pozwala na”, „umożliwia nie tylko…, ale także…” powtarzane | „umożliwia”, raz, z dopełnieniem |
| „efektywny”, „sprawny”, „optymalny” bez miary | miara (czas, liczba kroków, liczba błędów) |
| „Podsumowując,”, „Reasumując,”, „Wnioskując,” na końcu sekcji | brak podsumowania; wnioski tylko w sekcji „Wnioski” |
| „Mamy nadzieję, że”, „Z pewnością” | nic |

**Kalki z angielskiego**

| Kalka | Poprawnie |
|---|---|
| „adresować problem” | „rozwiązywać problem”, „odpowiadać na problem” |
| „na bazie” (= na podstawie) | „na podstawie” |
| „implementować funkcjonalność” (o planie) | „zaprojektować funkcję”; „zaimplementować” tylko o kodzie |
| „wspierać” (= obsługiwać) | „obsługiwać”, „umożliwiać” |
| „dedykowany” (= przeznaczony) | „przeznaczony dla”, „osobny” |
| „bazować na” | „opierać się na” |
| „w oparciu o” nadużywane | „na podstawie”, „z~użyciem” |
| „user”, „feature”, „deploy” w tekście | „użytkownik”, „funkcja”, „wdrożenie” (nazwy techniczne w `\texttt{}`) |

**Wzorce składniowe**

- Triady przymiotników („prosty, intuicyjny i niezawodny”) — zostaje jeden, sprawdzalny, albo żaden.
- Pytania retoryczne („Jak zatem ograniczyć straty?”).
- Puste wstępy („W niniejszym rozdziale zostaną przedstawione zagadnienia związane z…”) i puste zakończenia powtarzające treść.
- Listy punktowane tam, gdzie jest ciąg przyczynowo-skutkowy. Lista tylko dla wyliczeń równorzędnych elementów (role, wymagania, kroki scenariusza). Opis sklepu, uzasadnienia i wnioski piszę się prozą.
- Pogrubienie w tekście ciągłym. Wolno: nazwa elementu w definicji listy (`\textbf{Klient-obserwator} -- …`), nagłówki tabel. W akapicie nie pogrubia się nic.
- Łańcuchy myślników („system — prosty — działa…”). Myślnik (`--`) najwyżej raz w zdaniu; zwykle przecinek albo dwa zdania.
- Zdania-echa: następne zdanie mówi to samo innymi słowami.
- Asekuracje („może potencjalnie”, „w pewnym stopniu”) — albo fakt, albo jawne założenie.
- Antropomorfizacja systemu („system dba o”, „system rozumie”).

## Jak wygląda dobra sekcja

1. **Zdanie wprowadzające**: co sekcja zawiera, bez formułki („W tej części…”). Przykład (liczby w nawiasach ostrych podaje Karol): „Sklep zatrudnia ⟨N⟩ osób, a~towar przyjmuje od ⟨M⟩ dostawców; poniżej opisano przebieg dnia pracy i~miejsca, w~których powstają straty.”
2. **Treść**: akapity w porządku logicznym (kto → co robi → jakie dane → jakie reguły), konkretne przykłady z warzywniaka.
3. **Rysunki i tabele**: każdy ma `\caption` i `\label` i jest przywołany w tekście przed miejscem wstawienia (`tab.~\ref{tab:swot}`, `rys.~\ref{fig:pu-rezerwacje}`). Tekst mówi, co z rysunku/tabeli wynika („Z~tab.~\ref{tab:swot} wynika, że główne ryzyko leży po stronie czasu wdrożenia”), a nie przepisuje jego zawartość. Rysunek bez odwołania w tekście usuwa się.
4. **Bez powtórzeń między sekcjami**: informacja pada raz, w sekcji, do której należy; gdzie indziej odwołanie (`zob. p.~\ref{sec:zakres}`). Przed pisaniem przeczytaj sąsiednie, już napisane sekcje.
5. **Brak podsumowania** na końcu podsekcji. Ostatnie zdanie niesie treść (np. konsekwencję dla projektu).

## Logika wywodu: jak jest → dlaczego → co zmienia system

Raport prowadzi czytelnika jak „Sklep hydrauliczny”: od obecnego świata do systemu (struktura: skill `zrodla-sprawozdania`, `docs/plan-sprawozdania.md` §1).

- **1.1 Obecny sposób działania sklepu** opisuje wyłącznie stan dzisiejszy, w czasie teraźniejszym („właściciel składa zamówienie telefonicznie”). Nie pojawiają się tu funkcje systemu ani zdania „system umożliwi”.
- **1.2 Problemy** wynikają z opisu z 1.1 i odwołują się do niego; przy każdym problemie wolno jednym zdaniem wskazać mechanizm systemu, ze szczegółami w 1.3.
- **1.3 Proponowany system** zaczyna od zdania przejścia od problemów do zmian, potem opisuje reguły pracy po wdrożeniu w czasie teraźniejszym („rezerwację składa się…”) i mówi, co zostaje bez zmian.
- **Rozdz. 2** (cel, wymagania) nie powtarza opisu z 1.3: cel odwołuje się do P1–P8 (`\ref{prob:…}`), wymagania przekładają reguły z 1.3 na numerowane funkcje.
- Fakt pada raz, w sekcji, do której należy; w innych miejscach odwołanie `p.~\ref{}`.

## Etap 1 — pisanie od nowa

Decyzja Karola Q2 (03.11.2026): etap 1 powstaje od zera. **Nigdy nie wklejaj ani nie parafrazuj zdanie po zdaniu dawnej treści z git** (`git show HEAD:dokumentacja/rozdzialy/01-analiza.tex` ani żadnej innej rewizji). Fakty z tamtej wersji (oznaczone [H01] w `docs/`) wolno użyć dopiero, gdy Karol potwierdzi je w rozmowie o danej sekcji; tekst pisze się wtedy na nowo.

## Typografia polska w LaTeX

- Twarde spacje po jednoliterowych spójnikach i przyimkach: `a~`, `i~`, `o~`, `u~`, `w~`, `z~` (także na początku zdania: `W~sklepie`).
- Twarde spacje w skrótach i odwołaniach: `rys.~\ref{}`, `tab.~\ref{}`, `p.~\ref{}`, `dr~inż.`, `np.~`, liczba i jednostka `20~kg`.
- Cudzysłów polski „…” (w źródle `„…”` jako znaki UTF-8). Myślnik `--` ze spacjami, łącznik `-` bez spacji, zakres liczb `19--30.11`.
- Daty `17.11.2026`; godziny `8:00--18:00`.
- Nazwy plików, poleceń, modeli i pól w `\texttt{}` (`\texttt{Rezerwacja}`, `\texttt{manage.py migrate}`).

## Konwencje LaTeX w `dokumentacja/sprawozdanie.tex`

- Jeden plik, bez `\input`. Rozdziały (na wzór „Sklepu hydraulicznego”, szkielet w `docs/plan-sprawozdania.md` §1) = `\section` poprzedzone `\clearpage`, z `\label{ch:…}`; elementy = `\subsection` / `\subsubsection`. Nienumerowana „Specyfikacja projektu” (`\section*` + `\addcontentsline`) zostaje pusta z `% TODO` do końca prac. Nie zmieniaj nagłówków ani etykiet bez prośby Karola.
- Etykiety z prefiksem: `sec:`, `tab:`, `fig:`, `lst:`.
- Tabele: `booktabs` (`\toprule`/`\midrule`/`\bottomrule`), bez pionowych linii, podpis nad tabelą; długie — `longtable` z `\endfirsthead`/`\endhead`.
- Rysunki: pliki w `dokumentacja/figury/` (PDF/PNG; źródła diagramów obok, np. `.drawio`, `.puml`). Wstawianie przez `figure` + `\includegraphics` + `\caption` + `\label`. Makro `\figura` nie ma `\label` — nie używaj go, dopóki nie zostanie rozszerzone. Brak pliku → `% TODO: rysunek <nazwa>`; nie wymyślaj grafiki.
- Kod: `lstlisting` z `caption` i `label`, maks. ~30 linii, `language=Python` / `SQL` / `bash`.
- Strona tytułowa i spis treści są ustalone (jedna polska strona tytułowa bez logo, czarne linie, nagłówek uczelni i wydziału, tytuł „Dokumentacja techniczna: aplikacja webowa lokalnego sklepu warzywnego”, autorzy z indeksami, prowadzący, słowa kluczowe, „WROCŁAW 2026”; spis treści z numeracją rzymską, treść od 1). Nie zmieniaj ich bez prośby; przy zmianie składu lub tytułu edytuj istniejący blok, nie składaj strony od nowa.
- Kompilacja i kontrola: patrz `CLAUDE.md` § „Budowanie PDF”.

## Samokontrola przed oddaniem sekcji

Przejdź listę na gotowym tekście (nie na planie) i popraw, zanim pokażesz go Karolowi:

1. Wyszukaj w tekście frazy z tabel „Zakazane AI-izmy” (np. `kluczow`, `warto (zauważ|podkreśl|wspomn|zaznacz)` — samo `warto` trafia też w „wartość”, `kompleks`, `innowac`, `istotn`, `Podsumow`, `w oparciu`, `dedykowan`). Każde trafienie przepisz albo uzasadnij.
2. Czy pierwsze zdanie sekcji mówi, co zawiera, i nie jest formułką?
3. Czy każdy akapit ma jedną myśl, a każde twierdzenie odnosi się do warzywniaka lub źródła?
4. Czy każda liczba pochodzi od Karola, ze źródła albo z uruchomionego polecenia? Czy brakujące mają `% TODO`?
5. Czy każdy rysunek i tabela ma podpis, etykietę, odwołanie w tekście i zdanie interpretacji?
6. Czy nic nie powtarza treści innej sekcji? Czy terminy są te same co w sekcjach wcześniejszych?
7. Czy jest najwyżej jedna lista punktowana na podsekcję i czy nie zastępuje ona prozy?
8. Czy w akapitach nie ma pogrubień, pytań retorycznych, triad przymiotników i zakończenia „Podsumowując”?
9. Forma bezosobowa w całości; twarde spacje (`grep -nP ' [aiouwzAIOUWZ] ' dokumentacja/sprawozdanie.tex` nie zwraca nowych trafień).
10. PDF kompiluje się bez błędów i niezdefiniowanych odwołań.
