# Zasady pisania sprawozdania IBD

Jak pisać `dokumentacja/sprawozdanie.tex`, żeby był to raport gotowy do oddania prowadzącemu, a nie zapis rozmowy z modelem językowym. Plik obowiązuje każdego, kto pisze lub poprawia tekst sprawozdania: członków grupy i agenta (Claude Code). Jest importowany w `CLAUDE.md`, więc agent ma go zawsze w kontekście.

Kolejność ważności przy sprzeczności:

1. `materialy/IDB_wytyczne_v4.pdf` (wytyczne prowadzącego) i notatka z konsultacji 19.10.2026.
2. Decyzje Karola z dziennika w `CLAUDE.md`.
3. Ten plik.
4. Skille `styl-sprawozdania` i `zrodla-sprawozdania` (szczegóły, konwencje LaTeX-a, gdzie szukać faktów).

Ten plik zbiera zasady w jednym miejscu; skille ich nie zastępują ani nie uchylają.

---

## 1. Dla kogo jest tekst

Czytelnikiem jest prowadzący (dr inż. Roman Ptak), który zna bazy danych, UML i Django lepiej niż autorzy, ale nie zna warzywniaka i nie widział rozmów w grupie. Z tego wynikają trzy reguły:

1. **Tekst czyta się bez kontekstu rozmowy.** Każde zdanie ma sens dla kogoś, kto widzi tylko PDF. Nie ma w nim odniesień do pytań Q1–Q14, punktów dziennika decyzji, „ustaleń z Karolem”, promptów, agenta ani wersji pliku.
2. **Tekst nie tłumaczy rzeczy oczywistych dla specjalisty.** Nie wyjaśnia się, czym jest klucz obcy, ORM czy transakcja. Wyjaśnia się, dlaczego w tym systemie zrobiono tak, a nie inaczej.
3. **Tekst jest dokumentem grupy, nie odpowiedzią.** Nie zaczyna się od „Oto…”, „Poniżej przedstawiono…”, nie kończy się podsumowaniem tego, co właśnie napisano, nie proponuje „dalszych kroków” i nie pyta czytelnika o nic.

Test: gdyby jedną stronę wydrukować i dać osobie spoza grupy, czy uzna ją za fragment pracy studenckiej, czy za wklejoną odpowiedź czatu? Jeśli za to drugie, strona wymaga przepisania.

## 2. Poziom merytoryczny

Docelowy poziom: dobra praca inżynierska lub tekst doktoranta w dokumentacji projektu. W praktyce oznacza to:

- **Każda decyzja ma uzasadnienie i odrzuconą alternatywę.** Nie „wybrano MySQL”, lecz „wybrano MySQL 8.4 zamiast SQLite, ponieważ SQLite blokuje całą bazę przy zapisie, a rezerwacje wielu klientów przed 18:00 trafiają do tej samej tabeli”.
- **Twierdzenie jest sprawdzalne.** Podaje się liczbę, warunek, nazwę tabeli, numer wymagania albo przypadku użycia. „System jest wydajny” nie jest twierdzeniem; „lista produktów ładuje się w ≤ 2 s przy 22 jednoczesnych użytkownikach (WN5)” jest.
- **Terminy są precyzyjne i stałe.** Jedno pojęcie, jedno słowo w całym raporcie (lista ustalonych terminów: skill `styl-sprawozdania`, „Rejestr” pkt 4). Synonimów dla urozmaicenia nie stosuje się: „rezerwacja” nie zmienia się w „zamówienie”, „rezerwację klienta”, „zgłoszenie”.
- **Fakty mają źródło.** Fakt o sklepie pochodzi z wywiadu z właścicielem (w raporcie: „ustalono w wywiadzie z właścicielem sklepu”), z dokumentacji technologii albo z uruchomionego polecenia. Nic nie jest wymyślone; brak danych zostaje w komentarzu `% TODO` i jest pytaniem do zespołu.
- **Spójność śledzi się w numerach.** WF ↔ PU ↔ tabele ↔ testy odwołują się do siebie przez `\ref`, a nie przez przepisane numery.
- **Ograniczenia mówi się wprost.** Jeśli czegoś nie zrobiono albo zrobiono uproszczenie (np. symulowana rejestracja karty), raport to nazywa i podaje powód.

## 3. Układ raportu i sekcji

Szkielet raportu (wzór: „Sklep hydrauliczny”) i mapa wymagań wytycznych są w `docs/plan-sprawozdania.md` §1. Tok wywodu: jak jest → dlaczego potrzebny jest system → co system zmienia → cel i wymagania → uzasadnienie i organizacja → przypadki użycia → baza → implementacja → testy → wdrożenie → wnioski.

Każda sekcja:

1. **Zaczyna się od zdania z treścią**, które mówi, czego dotyczy sekcja, przez fakt, a nie zapowiedź. Źle: „W niniejszym rozdziale zostaną przedstawione wymagania funkcjonalne systemu.” Dobrze: „Wymagania funkcjonalne pogrupowano według ról, w kolejności, w jakiej użytkownik spotyka się z systemem: konta, uwierzytelnianie, funkcje personelu, funkcje klienta.”
2. **Ma akapity z jedną myślą** (3–6 zdań), w porządku: kto → co robi → na jakich danych → według jakich reguł → co z tego wynika.
3. **Nie powtarza innych sekcji.** Fakt pada raz, w miejscu, do którego należy; gdzie indziej jest odwołanie `p.~\ref{…}`.
4. **Kończy się treścią**, nie podsumowaniem. Ostatnie zdanie niesie konsekwencję albo ostatni fakt.
5. **Ma najwyżej jedną listę punktowaną** i tylko dla elementów równorzędnych (role, wymagania, kroki scenariusza). Przyczyny, uzasadnienia, opis sklepu i wnioski pisze się prozą.

## 4. Język i styl

- **Forma bezosobowa** w całym raporcie: „zaprojektowano”, „przyjęto”, „system zapisuje”. Bez „my”, „nasz zespół”, „zaprojektowaliśmy”.
- **Czas:** przeszły dla prac wykonanych („przeprowadzono wywiad”), teraźniejszy dla sklepu i systemu („sprzedawca przyjmuje dostawę”).
- **Zdania:** średnio 15–25 słów, zdania powyżej 35 słów dzieli się. Długość zdań ma się różnić; ciąg zdań o identycznej budowie („System… . System… . System… .”) przepisuje się.
- **Strona czynna, gdy wykonawca jest znany**: „sprzedawca wydaje rezerwację”, nie „dokonywane jest wydanie rezerwacji przez sprzedawcę”.
- **Czasowniki zamiast rzeczowników odczasownikowych**: „po zważeniu towaru sprzedawca…”, nie „po dokonaniu czynności ważenia towaru…”.
- **„Jest” i „ma” są w porządku.** Nie zastępuje się ich na siłę przez „stanowi”, „pełni funkcję”, „służy jako”, „posiada”, „charakteryzuje się”.
- **Rejestr akademicko-techniczny, bez potocyzmów** („ogarnąć”, „sporo”, „fajnie”) i bez języka marketingu („nowoczesny”, „innowacyjny”, „bezproblemowy”).
- **Polska poprawność:** „na podstawie” (nie „na bazie”), „mieć” (nie „posiadać” o rzeczach abstrakcyjnych), „funkcja” (nie „funkcjonalność”, chyba że w sensie zbioru funkcji), „w celu” najwyżej raz na akapit, „dokonać” praktycznie nigdy.

## 5. Zwroty typowe dla tekstu generowanego przez AI

Poniższe zwroty pojawiają się w tekstach modeli językowych nieproporcjonalnie często (zestawienia: Wikipedia „Signs of AI writing”, polskie omówienia, sekcja 13). Pojedyncze wystąpienie nie jest błędem gramatycznym, ale nagromadzenie od razu zdradza tekst wygenerowany. W raporcie się ich nie używa; jeśli trafiły do szkicu, zdanie przepisuje się tak, żeby niosło fakt.

### 5.1. Wypełniacze i zapowiedzi

| Nie pisz | Zamiast tego |
|---|---|
| „Warto zauważyć, że”, „Należy podkreślić, że”, „Warto wspomnieć”, „Co istotne”, „Należy pamiętać, że”, „Trzeba zaznaczyć” | samo twierdzenie |
| „W niniejszym rozdziale zostaną przedstawione…”, „Poniżej przedstawiono…”, „Oto…”, „W tej sekcji omówimy…” | zdanie z treścią (p. 3) |
| „Jak widać”, „Jak wspomniano wcześniej”, „Jak już zostało powiedziane” | odwołanie `p.~\ref{}` albo nic |
| „W dzisiejszych czasach”, „W dobie cyfryzacji”, „W erze”, „Coraz więcej” | konkretna data, liczba albo nic |
| „Podsumowując”, „Reasumując”, „Wnioskując”, „Finalnie”, „Ostatecznie” | brak podsumowania; wnioski tylko w rozdz. „Wnioski” |
| „Mamy nadzieję”, „Z pewnością”, „Bez wątpienia”, „Niewątpliwie” | nic |
| „Co więcej”, „Dodatkowo”, „Ponadto”, „Jednocześnie” na początku kolejnych zdań | zwykle nic; spójnik tylko, gdy wnosi relację logiczną |

### 5.2. Słowa nadmuchane i oceniające

| Nie pisz | Zamiast tego |
|---|---|
| „kluczowy”, „kluczowe znaczenie”, „odgrywa kluczową rolę”, „stanowi istotny element” | co dokładnie robi i dla kogo; „kluczowy” tylko o kluczu w bazie |
| „istotny”, „znaczący”, „fundamentalny”, „niezwykle ważny” | dlaczego ważny: skutek z liczbą |
| „kompleksowy”, „innowacyjny”, „nowoczesny”, „zaawansowany”, „intuicyjny”, „przyjazny użytkownikowi”, „bezproblemowy”, „płynny”, „solidny”, „holistyczny” | funkcja, którą system ma, i miara |
| „efektywny”, „sprawny”, „optymalny”, „wydajny” bez miary | czas, liczba kroków, liczba błędów |
| „szeroki wachlarz”, „szereg możliwości”, „wiele korzyści”, „bogata funkcjonalność” | lista konkretnych funkcji |
| „rozwiązanie” jako nazwa wszystkiego | „system”, „aplikacja”, „moduł”, „tabela” |
| „ekosystem”, „synergia”, „paradygmat”, „krajobraz”, „podróż użytkownika” | nic albo zwykłe słowo |
| „zapewnia”, „gwarantuje”, „dba o” w odniesieniu do systemu | co system robi: „blokuje”, „sprawdza”, „odrzuca” |

### 5.3. Kalki z angielskiego

| Kalka | Poprawnie |
|---|---|
| „adresować problem” | „rozwiązywać problem” |
| „na bazie” (= na podstawie), „bazować na” | „na podstawie”, „opierać się na” |
| „w oparciu o” (nadużywane) | „na podstawie”, „z~użyciem” |
| „dedykowany” | „przeznaczony dla”, „osobny” |
| „wspierać” (= obsługiwać) | „obsługiwać”, „umożliwiać” |
| „implementować funkcjonalność” (o projekcie) | „zaprojektować funkcję”; „zaimplementować” tylko o kodzie |
| „zagłębić się w”, „eksplorować”, „uwypuklić” | „opisać”, „zbadać”, „pokazać” |
| „w kontekście”, „na poziomie”, „w ramach” powtarzane | konkretny przyimek albo przebudowa zdania |
| „user”, „feature”, „deploy”, „flow”, „use case” w prozie | „użytkownik”, „funkcja”, „wdrożenie”, „przebieg”, „przypadek użycia” |

### 5.4. Wzorce składniowe

- **Triady.** „prosty, intuicyjny i niezawodny”, trzy przykłady tam, gdzie wystarczy jeden. Zostaje jeden sprawdzalny przymiotnik albo żaden; wylicza się tyle elementów, ile jest naprawdę.
- **Paralelizmy przeczeń.** „nie tylko…, ale także…”, „to nie jest X, lecz Y”, „zamiast X — Y”. Pisze się wprost, co jest.
- **Doklejone imiesłowy.** Zdanie zakończone „…, zapewniając spójność danych”, „…, umożliwiając klientom…”, „…, co przekłada się na…”. Taki dopisek zwykle nie niesie faktu; skutek, jeśli jest ważny, idzie do osobnego zdania z konkretem.
- **Łańcuchy „dzięki temu”.** „Dzięki temu… Dzięki temu… Pozwala to…” Jedno zdanie skutku na akapit wystarczy.
- **Myślniki.** Najwyżej jeden myślnik (`--`) w zdaniu, a w akapicie rzadko. Zwykle lepszy jest przecinek albo dwa zdania.
- **Pytania retoryczne** („Jak zatem ograniczyć straty?”) i wykrzykniki.
- **Zdania-echa.** Następne zdanie mówi to samo innymi słowami. Usuwa się jedno z nich.
- **Asekuracje.** „może potencjalnie”, „w pewnym stopniu”, „do pewnego stopnia”, „wydaje się, że”. Albo fakt, albo jawne założenie („przyjęto, że…”).
- **Ogólnikowe autorytety.** „Eksperci wskazują”, „badania pokazują”, „powszechnie uważa się”. Albo konkretne źródło w bibliografii, albo nic.
- **Optymistyczne zakończenia.** „Mimo wyzwań projekt otwiera drogę do…”, „stanowi solidny fundament dla przyszłego rozwoju”. Wnioski nazywają konkretną rzecz i jej skutek (wzór: „Sklep hydrauliczny”, rozdz. 10).
- **Antropomorfizacja.** „system rozumie”, „system dba”, „aplikacja wie”.

### 5.5. Formatowanie zdradzające czat

- Pogrubienia w tekście ciągłym. Wolno tylko w nagłówkach tabel i jako nazwa elementu w liście definicji (`\textbf{Klient-obserwator} -- …`).
- Nagłówki z dwukropkiem i podtytułem („Rezerwacje: jak to działa”), nagłówki w formie pytań, emotikony, symbole ✅ ❌ →.
- Listy punktowane zagnieżdżone w listach, listy w miejscu prozy, każdy akapit zamieniony w punkty.
- Składnia Markdown w LaTeX-u (`**tekst**`, `` `kod` ``, `#`), angielskie cudzysłowy "…" zamiast „…”.

## 6. Skróty i zapisy skrótowe

Skróty utrudniają czytanie, jeśli czytelnik musi je zgadywać. Zasady:

1. **Skróty projektowe** (WF, WN, PU, ERD, ORM, UML, CSF, SWOT, DDL, CSRF, HTTPS, LAN, SMTP, WSGI) rozwija się przy pierwszym użyciu: „wymagania funkcjonalne (WF)”. Jeśli raport będzie miał wykaz skrótów, każdy użyty skrót się w nim znajduje.
2. **Standardowe skróty polskie** (np., m.in., tzn., tj., tzw., ok., wg, zob., p., rys., tab., rozdz.) wolno stosować, oszczędnie i z twardą spacją po nich (`np.~`, `rys.~\ref{}`). W tekście ciągłym lepiej „według” niż „wg”, „około” niż „ok.” przy liczbach bez jednostki.
3. **„itd.”, „itp.”, „etc.” nie zamykają wyliczenia**, które powinno być pełne. Jeśli lista jest pełna, kończy się ostatnim elementem; jeśli przykładowa, zaczyna się od „np.” albo „m.in.” i nie ma na końcu „itp.”.
4. **Nie stosuje się skrótów ad hoc i potocznych:** „dot.”, „nt.”, „ww.”, „j.w.”, „bd.”, „b/d”, „spr.”, „zam.”, „rez.”, „dost.”, „info”, „admin” (poza nazwą `Django Admin`), „apka”, „baza” w znaczeniu bazy danych tam, gdzie może być niejasne.
5. **Symbole nie zastępują słów w prozie:** „/” zamiast „lub” albo „i” („klient/sprzedawca”), „+” zamiast „i”, „&”, „→”, „=>”, „~” jako „około”, „x” jako „razy”, „vs”. W prozie pisze się słowami; strzałki tylko na diagramach.
6. **Skrótów angielskich nie używa się, gdy jest polski termin:** „wersja minimalna” zamiast „MVP”, „wdrożenie” zamiast „deploy”. Nazwy własne technologii (Django, MySQL, InnoDB, Gunicorn) zostają.
7. **Nazwy z kodu** (`select_for_update`, `transaction.atomic`, `pozycja_rezerwacji`) pisze się w `\texttt{}` i przy pierwszym użyciu objaśnia jednym zdaniem.

## 7. Zapisy robocze, które nie mogą trafić do raportu

Notatka `do_poprawy_karol.md` (pkt 5) wymienia osobno „skrótowe i bezsensowne zapisy, szczególnie w typie komentarza dla siebie”. To są zapisy, które mają sens tylko dla autora albo agenta:

| Zapis roboczy w tekście | Jak w raporcie |
|---|---|
| „(Q3)”, „zgodnie z Q7”, „pkt 56”, „decyzja z 04.11” | nic; decyzję opisuje się przez jej uzasadnienie |
| „W4 pkt 7”, „N19 uwaga 1”, „SH rozdz. 5” | „wytyczne prowadzącego zalecają…”, „podczas konsultacji 19.10.2026 prowadzący zwrócił uwagę…”, wzór formy się nie cytuje |
| „(Karol)”, „ustalone z Karolem”, „do akceptacji”, „propozycja agenta” | „ustalono w wywiadzie z właścicielem sklepu” albo nic |
| „TODO”, „do uzupełnienia”, „xxx”, „???”, „[…]” w widocznym tekście | tylko komentarz LaTeX-a `% TODO: …`; przed oddaniem żadnego nie ma |
| „plan → dostawa → stan” w zdaniu | „dostawę porównuje się z planem, a stan wynika z dostaw i sprzedaży” |
| „rez. na D+1…D+7” | „rezerwacje na dni od następnego do siódmego dnia po dniu złożenia” |
| hasła zamiast zdań: „Blokada: zaległość > 100 zł.” | „Klient, którego zaległość przekracza 100~zł, nie może składać nowych rezerwacji.” |
| nawiasy z dygresjami „(patrz wyżej)”, „(jak ustalono)”, „(nowe)”, „(zmienione)” | odwołanie `\ref` albo nic; raport nie opisuje historii swoich wersji |
| „w tej wersji raportu”, „poprawiono”, „zaktualizowano” | nic; raport opisuje system, nie zmiany w raporcie |

Komentarze `%` w pliku `.tex` mogą zawierać notatki robocze, bo nie trafiają do PDF. Treść widoczna w PDF nie może.

## 8. Liczby, jednostki, daty

- Liczba z jednostką i twardą spacją: `20~kg`, `100~zł`, `2~s`, `15~W`. Procent: `10\%`.
- Liczby od Karola, z wywiadu, z dokumentacji albo z uruchomienia. Szacunek nazywa się szacunkiem i podaje się, na czym go oparto.
- Daty `17.11.2026`, godziny `6:00`, zakresy `6:00--18:00`, `19--30.11`.
- Kwoty z separatorem tysięcy jako twardą spacją: `11~050~zł`; ułamki z przecinkiem: `2,5~kg`.
- Wyników testów i pomiarów nie podaje się, dopóki nie zostały uruchomione. Wtedy podaje się polecenie, środowisko i datę.

## 9. Rysunki, tabele, listingi

- Każdy rysunek i tabela ma podpis (tabela nad, rysunek pod), etykietę i odwołanie w tekście przed miejscem wstawienia.
- Podpis pozwala zrozumieć rysunek bez czytania tekstu: „Diagram przypadków użycia modułu Rezerwacje”, nie „Diagram”.
- Tekst mówi, co z rysunku lub tabeli wynika, a nie przepisuje jego zawartość. Rysunek bez odwołania usuwa się.
- Tabele `booktabs`, bez pionowych linii; jednostki w nagłówkach kolumn.
- Listing kodu ≤ 30 linii, z podpisem, i akapit o tym, co fragment robi i dlaczego tak.
- Zrzuty ekranu i diagramy czytelne po wydruku: tekst na rysunku nie mniejszy niż przypis.

## 10. Źródła

- Fakty o sklepie: wywiad z właścicielem (w grupie właściciela odgrywał Mateusz Złośnik, zob. p. 3.6.2 raportu); w raporcie „właściciel sklepu”, bez nazwisk grupy.
- Fakty techniczne (wersje, licencje, mechanizmy Django i InnoDB): oficjalna dokumentacja, z pozycją w bibliografii, jeśli bibliografia powstanie (Q14).
- Przykładowe raporty z `materialy/` dają formę, nie treść; nie cytuje się ich i nie przepisuje.
- O sobie (AI, agent, czat) raport nic nie mówi. Jeśli wytyczne lub prowadzący będą wymagać deklaracji użycia narzędzi AI, jej treść ustala zespół.

## 11. Przykłady: przed i po

Przykłady pokazują formę. Fakty w nich (np. lista aktorów, zdanie z wniosków) są ilustracją i nie zastępują ustaleń projektu.

> Źle: „Warto zauważyć, że system odgrywa kluczową rolę w ograniczaniu strat, zapewniając właścicielowi kompleksowy wgląd w popyt.”
>
> Dobrze: „Rezerwacje na następny dzień kończą się o 18:00, więc właściciel składa zamówienie u dostawcy, znając zarezerwowaną część popytu.”

> Źle: „Wybrano bazę MySQL (Q3, W4 pkt 7) → lepsza współbieżność niż SQLite.”
>
> Dobrze: „Zamiast SQLite wybrano MySQL 8.4 z silnikiem InnoDB. SQLite blokuje przy zapisie cały plik bazy, a InnoDB tylko zmieniane wiersze, co ma znaczenie, gdy kilku klientów rezerwuje ten sam produkt tuż przed 18:00.”

> Źle: „W niniejszym podrozdziale przedstawiono aktorów systemu. Aktorzy stanowią istotny element modelu przypadków użycia.”
>
> Dobrze: „System ma trzech aktorów-ludzi: klienta, sprzedawcę i właściciela, oraz trzech aktorów zewnętrznych: czas, operatora płatności i serwer poczty (tab.~\ref{tab:aktorzy}).”

> Źle: „Podsumowując, projekt nie tylko spełnia założenia, ale także stanowi solidny fundament do dalszego rozwoju.”
>
> Dobrze (rozdz. „Wnioski”): „Nie zrealizowano zestawień właściciela z wersji rozszerzonej, ponieważ czas między 17.11 a 30.11 wystarczył na wersję standardową; bez nich różnicę między planem a dostawą właściciel sprawdza w panelu dzień po dniu.”

## 12. Kontrola przed oddaniem sekcji i całości

Na gotowym tekście, nie na planie:

1. Przeczytać sekcję na głos albo w PDF, jak prowadzący. Każde zdanie, które nic nie mówi o warzywniaku ani o systemie, usunąć.
2. Uruchomić wyszukiwanie zwrotów z p. 5–7 (niżej) i każde trafienie przepisać albo świadomie zostawić.
3. Sprawdzić, czy każdy skrót jest rozwinięty przy pierwszym użyciu.
4. Sprawdzić, czy każda liczba ma źródło, a brakujące są tylko w `% TODO`.
5. Sprawdzić podpisy, etykiety i odwołania do rysunków i tabel.
6. Zbudować PDF (`CLAUDE.md`, „Budowanie PDF”), sprawdzić log: brak błędów, brak niezdefiniowanych odwołań.
7. Przed oddaniem całości: `grep -n 'TODO' dokumentacja/sprawozdanie.tex` nie zwraca nic poza świadomie zostawionymi komentarzami, w PDF nie ma ramek „TODO: brak pliku”.

Wyszukiwanie (z katalogu repozytorium; komentarze `%` są pomijane):

```bash
grep -niE \
 'warto (zauważ|podkreśl|wspomn|zaznacz)|należy (podkreślić|pamiętać|zaznaczyć)|co istotne|kluczow|istotn|kompleks|innowac|nowoczesn|zaawansowan|intuicyjn|bezproblem|solidn|holistyczn|efektywn|optymaln|szeroki wachlarz|szereg |podsumow|reasumuj|finalnie|w dzisiejszych|w dobie|w erze|niniejsz|poniżej przedstawiono|jak widać|jak wspomniano|nie tylko|odgrywa|stanowi |pełni (funkcj|rol)|posiada|dokona|funkcjonalnoś|w oparciu|na bazie|bazuj|dedykowan|adresow|zagłębi|w kontekście|zapewniając|umożliwiając|dzięki temu|co więcej|dodatkowo|ponadto|z pewnością|niewątpliwie|mamy nadzieję|eksperci|ekosystem|synergi' \
 dokumentacja/sprawozdanie.tex | grep -vE '^[0-9]+:\s*%'
grep -nE '\bQ[0-9]+\b|\bpkt [0-9]|\bN19\b|\bW4\b|\bSH\b|Karol|agent|do akceptacji|→|->|=>|\bitd\.|\bitp\.|\betc\.|\bdot\.|\bnt\.|\bww\.|\bMVP\b|\?\?|xxx|\*\*' \
 dokumentacja/sprawozdanie.tex | grep -vE '^[0-9]+:\s*%'
grep -nP ' [aiouwzAIOUWZ] ' dokumentacja/sprawozdanie.tex | grep -vE '^[0-9]+:\s*%'   # brak twardych spacji
```

Trafienie nie zawsze jest błędem („klucz główny”, „istotność” w sensie statystycznym, „posiada” w cytacie, nazwiska autorów na stronie tytułowej przy wzorcu `Karol`). Decyduje czytający, ale każde trafienie trzeba obejrzeć.

## 13. Źródła tych zasad

- Wytyczne prowadzącego: `materialy/IDB_wytyczne_v4.pdf`; notatka z konsultacji 19.10.2026; `do_poprawy_karol.md` (pkt 5 „Weryfikacja”).
- Wzory formy: „Sklep hydrauliczny – przykładowy raport” (rozdz. 2.1 cel z „Uwagą”, rozdz. 10 wnioski) i kontrprzykład „Szkółka narciarska” (rozdz. 8), `materialy/bazdy danych/`.
- Wikipedia: [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (WikiProject AI Cleanup) – nadmuchane znaczenie, doklejone imiesłowy, unikanie „jest”, paralelizmy przeczeń, triady, myślniki, pogrubienia, optymistyczne zakończenia, ogólnikowe autorytety.
- Polskie omówienia: [android.com.pl – jak rozpoznać tekst napisany przez AI](https://android.com.pl/nauka/1073204-jak-rozpoznac-tekst-napisany-przez-ai/), [antyweb.pl – sztuczna inteligencja po polsku](https://antyweb.pl/sztuczna-inteligencja-po-polsku), [FlowHunt – AI Humanizer](https://www.flowhunt.io/pl/blog/ai-humanizer-guide/) („warto zauważyć”, „kluczowy”, „istotny”, „zagłębić się”, „co więcej”, „dodatkowo”, „nie tylko…, ale też…”).
- Pisanie sprawozdań: M. Zajusz, [„Podręcznik tresowania wielbłądów”](https://home.agh.edu.pl/~zajuszm/files/Jak-pisa--sprawozdania.pdf), AGH 2023 (język specjalistyczny, czas, twarde spacje, podpisy rysunków i tabel, jednostki); [Biblioteka PW – edycja i poprawność językowa](https://bg.pw.edu.pl/dane/e_learning/Cz_2_4_Edycja_i_poprawnosc_jezykowa_2022_08.pdf) (skróty).

Listy zwrotów z tych źródeł są orientacyjne: same w sobie nie dowodzą, że tekst napisał model. Celem nie jest „oszukanie detektora”, tylko tekst, który mówi coś konkretnego.
