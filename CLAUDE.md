# CLAUDE.md — sprawozdanie IBD „Lokalny warzywniak”

Główna instrukcja dla Claude Code w tym repozytorium. Jedno źródło prawdy dla agenta: ten plik + skille w `.claude/skills/` + plan i indeks w `docs/`. `README.md` to opis zewnętrzny repozytorium, nie instrukcja dla agenta.

## Projekt

- Przedmiot: Internetowe bazy danych, Politechnika Wrocławska, W4N, kierunek Informatyka techniczna. Prowadzący: dr inż. Roman Ptak.
- Grupa: Karol Gąsior 280913, Mikołaj Winiecki 280952, Mateusz Złośnik 281201. Z agentem pracuje Karol.
- Temat: aplikacja webowa jednego małego, stacjonarnego sklepu warzywnego. Cel biznesowy: mniej strat na psującym się towarze dzięki rezerwacjom konkretnych ilości z odbiorem osobistym. Bez dowozu i płatności online (płatność na miejscu). Poza zakresem bez wyraźnej prośby Karola: wiele sklepów, programy lojalnościowe, aplikacja mobilna, integracja z kasą, „pełny ERP”.
- Stack: Python + Django, baza SQLite (Q3 rozstrzygnięte 04.11.2026; MySQL/MariaDB tylko jako ścieżka rozwoju), uruchamiane na komputerze w sklepie, bez hostingu.
- Role: właściciel, sprzedawca (Django Admin), klient z kontem (osobny panel klienta), klient-obserwator (przegląd bez logowania), dostawca (bez konta — dostawy wprowadza personel; decyzja 04.11.2026). Operator płatności (karta klienta) należy do otoczenia systemu.
- Terminy laboratoriów: 19.10 analiza, 17.11 projekt, 30.11 implementacja i wdrożenie, 14.12 prezentacja.
- Produkt pracy: `dokumentacja/sprawozdanie.tex` (jeden plik LaTeX: Specyfikacja projektu + 14 rozdziałów w układzie i logice raportu „Sklep hydrauliczny” — jak jest → dlaczego system → co zmienia → cel i wymagania → uzasadnienie i organizacja → techniki modelowania → PU → baza → implementacja → testy → wdrożenie i podręcznik → prezentacja i zaliczenie → wnioski — przy czym każdy wymóg wytycznych v4 i notatki 19.10 ma własny nagłówek; szkielet, „Wzorzec SH” i tabela pokrycia w `docs/plan-sprawozdania.md` §1). Kodu aplikacji jeszcze nie ma.

## Zasady Karola (bezwzględne)

1. **Nie rób `git commit`, `git push`, PR ani zmian historii** (`reset`, `rebase`, `stash drop`, `checkout -- <plik>`). Commituje Karol. Dozwolone są tylko edycje plików w working tree; brudne drzewo jest normalne.
2. **Zapytaj przed usunięciem** lub przeniesieniem dowolnego pliku.
3. **Nie wymyślaj faktów**: cen, liczb, pomiarów, wyników testów, wersji, decyzji, danych o grupie. Brak danych → `% TODO: <czego brakuje, kto dostarcza>` w TeX-u i pytanie do Karola.
4. Odpowiadaj po polsku. Tekst sprawozdania: polski, forma bezosobowa, twarde spacje (`w~`, `i~`, `z~`…) — szczegóły w skillu `styl-sprawozdania`.
5. Zmieniaj tylko to, o co proszono. Jeden prompt = jedna sekcja/obowiązek; nie pisz kolejnej sekcji „przy okazji”.
6. Nie kasuj ani nie przebudowuj `materialy/` (źródła prowadzącego).

## Tryb pracy: sekcja po sekcji

Treść powstaje w rozmowie z Karolem, po jednej sekcji, w kolejności z `docs/plan-sprawozdania.md` §7 (etap 1: rozdz. 1, 2.1–2.2, 3), a dla dalszych rozdziałów wg §1–§3 planu.

1. **Przygotowanie** — przeczytaj w `docs/indeks-zrodel.md` wiersz danego podpunktu (część B), otwórz wskazane źródła i wzór formy. Przeczytaj już napisane sąsiednie sekcje `sprawozdanie.tex`.
2. **Omówienie** — pokaż Karolowi krótko: co sekcja ma zawierać wg wytycznych, jakie fakty już są (ze źródłem), czego brakuje (lista pytań, najwyżej kilka naraz, od najważniejszego), ewentualnie warianty do wyboru. Bez gotowego tekstu.
3. **Decyzje** — odpowiedzi Karola zapisz w dzienniku decyzji poniżej (data, numer pytania lub krótki opis). Jeśli coś przeczy notatce z konsultacji lub wytycznym, powiedz to przed pisaniem.
4. **Pisanie** — dopiero po omówieniu wpisz sekcję do `dokumentacja/sprawozdanie.tex`, stosując skill `styl-sprawozdania`. Zbuduj PDF i sprawdź log.
5. **Samokontrola i oddanie** — lista kontrolna ze skilla `styl-sprawozdania` i checklista ze skilla `zrodla-sprawozdania`. Pokaż Karolowi, co wpisano, i jakie `% TODO` zostały.
6. Następna sekcja dopiero na prośbę Karola.

Na prośbę „status” podaj: ostatnią omówioną/napisaną sekcję, następną wg §7 planu i otwarte pytania, które ją blokują. Nic nie edytuj.

## Dziennik decyzji

Pełna lista pytań z uzasadnieniem: `docs/plan-sprawozdania.md` §5. Tu tylko stan.

| Nr | Temat | Stan |
|---|---|---|
| Q1 | Zakres MVP | **Rozstrzygnięte 03.11.2026:** zakres z notatki 19.10 — rezerwacje z odbiorem osobistym, konta klientów, klient-obserwator i osobny panel klienta są w MVP; Django Admin tylko dla personelu. Założenie „system tylko dla personelu” jest nieaktualne. |
| Q2 | Dawna treść etapu 1 z git | **Rozstrzygnięte 03.11.2026:** etap 1 pisany od nowa. Nie przywracać i nie wklejać `git show HEAD:dokumentacja/rozdzialy/01-analiza.tex`. Statusy ✅ etapu 1 w `PLAN.md` są nieważne. |
| — | Tryb pracy | **Ustalone 03.11.2026:** sekcje omawiane z Karolem pojedynczo, potem pisane przez agenta. Dalsze pisanie w Claude Code (nie w Cursorze). |
| Q13 | Sprzątanie instrukcji agenta | **Zrobione 03.11.2026:** instrukcje w `CLAUDE.md` + `.claude/skills/`; `cursor.md` i `SKILL.md` usunięte (w git). |
| Q3 | SQLite czy MySQL | **Rozstrzygnięte 04.11.2026 (agent, wg preferencji Karola): SQLite.** W4 pkt 7 tylko zaleca MySQL, pkt 8 dopuszcza inne technologie; N19 uwaga 1 to ostrzeżenie bez wymogu. Obciążenie z `tab:parametry` (2 + do 20 użytkowników naraz, do 45 rezerwacji i ok. 220 sprzedaży dziennie) mieści się w szeregowaniu zapisów SQLite. Warunki: WAL, transakcje `IMMEDIATE`, `timeout`, sprawdzenie puli i zapis rezerwacji w jednej transakcji; MySQL/MariaDB jako ścieżka rozwoju. Opis w 3.3.2 (do napisania). Szczegóły: plan §5 Q3. |
| Q4 | Zestaw technik modelowania (UML + ERD + normalizacja) | otwarte |
| Q5 | Notacja ERD i narzędzie diagramów | otwarte |
| Q6 | Komputer w sklepie, dostęp klientów (LAN / internet) | otwarte |
| Q7 | Reguły rezerwacji, rola dostawcy | **Rozstrzygnięte 04.11.2026** — szczegóły pod tabelą. Opis słowny i parametry skalowalne napisane w `sprawozdanie.tex`. |
| — | Szkielet etapu 1 | **Zatwierdzone 04.11.2026:** „Grupa projektowa i podział obowiązków” przeniesiona tuż przed „Harmonogram”; dodano „Parametry skalowalne” pod „Opis słowny systemu”. Reszta szkieletu bez zmian (Q12). |
| — | Dostawca | **Rozstrzygnięte 04.11.2026:** dostawca nie ma konta w systemie; jego dostawy wprowadza personel (osoba otwierająca sklep). Dostawca nie jest aktorem systemu, tylko elementem otoczenia. |
| — | Operator płatności | **Rozstrzygnięte 04.11.2026:** operator płatności (rejestracja i obciążanie karty klienta) należy do otoczenia systemu. Opisane w 1.4 „Interesariusze i otoczenie systemu” (04.11.2026). |
| — | Przebudowa struktury | **Zrobione 04.11.2026 na prośbę Karola:** układ rozdziałów, nazwy i podział na wzór raportu „Sklep hydrauliczny” (`materialy/bazdy danych/`), przy zachowaniu wszystkich wymagań wytycznych v4 i uwag z notatki 19.10. Zachowano: „Grupa projektowa i podział obowiązków” tuż przed „Harmonogram”, „Parametry skalowalne”, P1–P8. Napisany tekst i `\label{}` przeniesione bez zmian. Kopia sprzed przebudowy: `dokumentacja/sprawozdanie.pre-restructure.tex.bak` (Karol może ją usunąć). Szkielet i tabela pokrycia: plan §1. |
| — | Osobne nagłówki dla wymogów wytycznych | **Zrobione 04.11.2026 na prośbę Karola:** każdy element W4 i N19 ma własny, rozpoznawalny nagłówek. Dodano: 2.2 Zakres projektu (wydzielony z celu), 3.3.1 Wybór technologii, wersje i licencje, 3.3.2 Współbieżne zapisy w bazie SQLite, 3.6.1 Skład grupy, 3.6.2 Podział obowiązków w etapach projektu, rozdz. 4 Techniki modelowania (4.1, 4.2), 6.5 Diagramy czynności wybranych PU (Q4), 7.1 Podejście code-first, 8.2 Środowisko programistyczne i repozytorium kodu, 8.4 Oddzielenie kodu od HTML – szablony Django, 13.1 Plan prezentacji, 13.2 Materiały przekazywane do zaliczenia. Przemianowano wg brzmienia wytycznych: rozdz. 1 „Opis słowny świata rzeczywistego”, 1.4 „…otoczenie podsystemu”, rozdz. 3 „Uzasadnienie potrzeby realizacji…”, 3.3 „Techniczna wykonalność systemu”, 3.4 „Koszt wytworzenia systemu (kosztorys)”, 7.3 „Model konceptualny (ERD)”, 7.6 „Słownik danych (definicje obiektów)”, 8.3 „Architektura trójwarstwowa”, 8.7 „Model fizyczny bazy danych”, rozdz. 12 „Wdrożenie aplikacji…”, 12.1.1–12.1.2 „…w sklepie”, rozdz. 13 „Prezentacja i zaliczenie projektu”. Tekst i etykiety bez zmian. Mapa: plan §1 „Pokrycie wymagań”. |
| — | Otoczenie systemu (1.4) | **Rozstrzygnięte 04.11.2026 (najprostsze warianty):** (1) zapłata za towar przy ladzie (gotówka lub terminal kartowy) poza systemem — system nie zapisuje płatności za sprzedaż, rozlicza tylko opłatę 10% za nieodebranie przez operatora płatności; (2) dostawca bez konta, w otoczeniu jako źródło dostaw wprowadzanych przez personel; (3) kasa fiskalna to osobne urządzenie bez integracji. Sekcja 1.4 napisana (`sec:otoczenie`, `tab:otoczenie`). |
| — | Druga przebudowa struktury | **Zrobione 04.11.2026 na prośbę Karola:** układ jeszcze ściślej wg SH. Rozdz. 1: 1.1 Obecny sposób działania sklepu (jak jest, `sec:opis`) → 1.2 Problemy P1–P8 (`sec:problemy`) → 1.3 Proponowany system (co wprowadza i zmienia, nowa `sec:system`) → 1.4 Interesariusze i otoczenie → 1.5 Parametry skalowalne. Rozdz. 2 „Cel projektu oraz wymagania systemu” (jak SH 2); SWOT…harmonogram w rozdz. 3 „Uzasadnienie i organizacja projektu”; architektura w 7.2 „Struktura systemu” (jak SH 6.1.2). Dawny „Opis słowny” rozdzielony na 1.1 i 1.3 bez utraty treści; dopisano zdania przejścia, odwołania w P1 i P5 wskazują teraz `sec:system`. Kopia: `dokumentacja/sprawozdanie.pre-restructure2.tex.bak` (Karol może usunąć). |
| Q8 | Wersje minimalna / standardowa / rozszerzona | otwarte |
| Q9 | Koszt wytworzenia (praca, sprzęt) | otwarte |
| Q10 | Wersje Pythona i Django | otwarte |
| Q11 | Nazewnictwo modeli PL/EN, sposób liczenia stanu | otwarte |
| Q12 | Nowy szkielet sprawozdania i przebudowa `PLAN.md` | **Szkielet zrobiony 04.11.2026** (wiersze „Przebudowa struktury” i „Druga przebudowa struktury” wyżej). Otwarte: przebudowa kolejki `PLAN.md` z przypisaniem osób. Dalszych zmian nagłówków nie rób bez prośby Karola. |
| Q14 | Literatura i spis rysunków | otwarte |

Przy nowej decyzji: zmień wiersz tutaj i oznacz pytanie w §5 planu jako rozstrzygnięte.

### Q7 — fakty od Karola (04.11.2026)

- Sklep czynny codziennie 6:00–18:00. Właściciel: Jan Nowak, osoba fizyczna prowadząca działalność gospodarczą. Osiedle we Wrocławiu, klienci z kilku bloków.
- Asortyment: podstawowe krajowe warzywa i owoce, bez zmian sezonowych; wszystko na wagę, bez sprzedaży na sztuki.
- Jeden dostawca, dostawa codziennie o 4:00; stan na dany dzień wynika z zamówienia z dnia poprzedniego; rezerwacje tylko z towaru dostępnego w sklepie w dniu odbioru.
- Dziś klienci nie mogą rezerwować; sklep trzyma duży zapas na nieregularne duże zakupy, co powoduje straty.
- Rezerwacja do 7 dni naprzód, zwykle na następny dzień; limit 20 kg na rezerwację (jedna skrzynka); odbiór do 18:00 dnia odbioru.
- Nieodebranie: utrata zadatku 10% wartości zamówienia. Rejestracja online z kartą płatniczą; zadatek pobierany po fakcie; przy zaległości > 100 zł klient nie może składać nowych rezerwacji.

### Q7 — uzupełnione przez agenta — do akceptacji Karola

1. **Plan dostawy jako pula rezerwacji:** dla każdego produktu i dnia ilość, którą właściciel zamówi; domyślnie standardowa dzienna ilość produktu; właściciel może ją zwiększyć lub zmniejszyć, ale nie poniżej ilości już zarezerwowanej. Do rezerwacji na dzień D zostaje plan na D minus zarezerwowane na D.
2. Rezerwacje na dni D+1…D+7 (bez rezerwacji na bieżący dzień).
3. Rezerwacje na dany dzień przyjmowane do 18:00 dnia poprzedniego; o tej godzinie właściciel składa zamówienie u dostawcy (telefonicznie) w ilościach z planu dostawy.
4. Bezpłatne anulowanie do 18:00 dnia poprzedniego; później anulować się nie da.
5. Jedna rezerwacja na klienta na dany dzień (żeby limitu 20 kg nie obchodzić wieloma rezerwacjami).
6. Towar pozostały z poprzedniego dnia idzie tylko do sprzedaży przy ladzie; rezerwacje realizuje się ze świeżej dostawy. Towar z nieodebranej rezerwacji trafia następnego dnia do sprzedaży przy ladzie.
7. Przy odbiorze klient płaci za rzeczywistą masę po cenie z dnia odbioru; wartość rezerwacji do opłaty 10% liczy się z zarezerwowanych ilości i cen z dnia odbioru.
8. Nazwa w raporcie: „opłata za nieodebranie rezerwacji”, przy czym zaznaczono, że właściciel nazywa ją zadatkiem (zadatek w sensie prawnym płaci się z góry).
9. Karta rejestrowana w formularzu operatora płatności; system przechowuje tylko identyfikator karty od operatora, bez numeru karty.
10. Opłaty tworzą zaległość klienta; właściciel raz w miesiącu obciąża karty przez operatora płatności poza systemem i odnotowuje wynik; zaległość można też zapłacić w sklepie (wpłatę odnotowuje sprzedawca).
11. Blokada przy zaległości > 100 zł obejmuje tylko nowe rezerwacje (złożone pozostają ważne) i ustaje samoczynnie, gdy zaległość spadnie do ≤ 100 zł.
12. Dane przy rejestracji: imię, nazwisko, e-mail, telefon, karta.
13. Personel: właściciel + 2 sprzedawców na zmianach 6:00–12:00 i 12:00–18:00; właściciel może wykonywać czynności sprzedawcy. (Zmienione 04.11 przy P7: dostawy o 4:00 nie przyjmuje nikt — patrz pkt 21.)
14. Dostawca nie ma konta w systemie; dostaje zamówienie przygotowane z planu dostawy.
15. W ciągu dnia nie ma dodatkowych dostaw.
16. Wszystkie wartości z tabeli parametrów skalowalnych (`sec:parametry` w `sprawozdanie.tex`), w tym przykładowa lista produktów, średni zakup przy ladzie 2,5 kg, maksymalna dostawa 1500 kg wynikająca z ładowności samochodu dostawcy oraz przyrost danych ok. 330 tys. wierszy rocznie.

### Problemy bez systemu (P1–P4, `sec:problemy`) — uzupełnione przez agenta — do akceptacji Karola

Od Karola: nadwyżka i psucie z powodu nieregularnych dużych zakupów, brak rezerwacji ilości, zamawianie na wyczucie, brak wiedzy o popycie na następny dzień (P1–P3).

17. P2 rozszerzony o braki popularnych produktów po południu po dużych zakupach rano.
18. P3 — liczby (szacunki): obecne zamówienie ok. 700 kg dziennie, czyli ok. 200 kg ponad typową sprzedaż przy ladzie 500 kg; ok. 40 kg dziennie traci świeżość (ok. 14,6 t rocznie); po wprowadzeniu rezerwacji typowa dostawa 650 kg (500 kg lada + 120 kg rezerwacje).
19. P4 w całości: stan oceniany na oko, brak zapisu dziennej sprzedaży per produkt, brak danych do ustalenia standardowych ilości i do pomiaru strat; rozwiązanie: ewidencja dostaw i sprzedaży (stan, historia, ilość niesprzedana).
20. Odrzucono jako niespójne z faktami Karola: telefoniczne umawianie dużych zakupów bez zobowiązania (Karol: dziś klienci w ogóle nie mogą rezerwować).

P5–P8 zatwierdził Karol (04.11.2026). Uzupełnione przez agenta — do akceptacji Karola:

21. Opis „jak jest”: dostawca ma klucz do zaplecza i zostawia towar o 4:00 bez udziału personelu; sklep otwiera ok. 5:30 zwykle właściciel, pod jego nieobecność sprzedawca z porannej zmiany; towaru nie porównuje się z zamówieniem; zamówienie telefoniczne nie jest zapisywane.
22. Ceny wypisane ręcznie na tabliczkach przy skrzynkach; sklep nie ma strony internetowej ani innego kanału informacji dla klientów.
23. Właściciel jako jedyna osoba składająca zamówienia i znająca stan; podczas jego nieobecności (choroba, urlop) zamawia sprzedawca z popołudniowej zmiany.
24. Godziny szczytu 6:00–9:00 i po 16:00; sklep nie zapisuje sprzedaży per produkt.
25. P6 — liczby (szacunki): w szczycie ok. połowa z 200 klientów dziennie, ok. 20 klientów na godzinę, jeden sprzedawca; zważenie i zapakowanie 15–20 kg trwa ok. 5 min.
26. Rezerwacje kompletuje, waży i pakuje sprzedawca poza godzinami największego ruchu; przy odbiorze zapłata za odważoną masę (zastępuje „waży przy odbiorze”).
27. W opisie systemu: osoba otwierająca sklep wprowadza ilości dostarczone, system porównuje je z planem dostawy; plan dostawy, stan i historia sprzedaży dostępne dla całego personelu; sprzedawca może złożyć zamówienie pod nieobecność właściciela.
28. Do P4 dołączono: brak śladu, od kiedy obowiązuje cena (tylko tabliczki), brak danych do inwentaryzacji i do porównania utargu ze sprzedanymi ilościami; system zapisuje cenę przy sprzedaży.
29. Tabela parametrów bez zmian.

### Interesariusze i otoczenie (1.4, `sec:otoczenie`) — uzupełnione przez agenta — do akceptacji Karola

Od Karola (04.11.2026): zapłata za towar poza systemem, dostawca bez konta, kasa fiskalna bez integracji, terminal kartowy przy ladzie.

30. Sprzedawca rejestruje sprzedaż dwukrotnie: w kasie fiskalnej i w systemie (wynika z braku integracji).
31. System zapisuje przy sprzedaży produkty, ilości i ceny, ale nie sposób ani kwotę zapłaty.
32. Zawartość kolumny „Wymiana z systemem” w `tab:otoczenie` (co każda rola wprowadza i otrzymuje) — złożona z ustaleń Q7 i P1–P8; nowe jest m.in. to, że sprzedawca widzi listę rezerwacji na dany dzień, a klient informację o blokadzie.
33. Prowadzącego i uczelni nie ujęto jako interesariuszy systemu (nie korzystają z aplikacji sklepu); jeśli Karol chce, można dodać zdanie o odbiorcy dokumentacji.

### Rozdz. 1 — uzupełnienia wg SH rozdz. 1 (atrybuty produktu, stany rezerwacji) — uzupełnione przez agenta — do akceptacji Karola

Dopisane 04.11.2026 na końcu 1.3 (`sec:system`), po liście ról. Źródło formy: SH rozdz. 1 (atrybuty produktu, stany zamówienia).

34. Produkt ma nazwę (z odmianą, gdy potrzeba), cenę za kilogram i standardową dzienną ilość; stan w kg system wyznacza z dostaw i sprzedaży.
35. Ceny zmienia właściciel; system zapisuje datę, od której cena obowiązuje, i cenę przy każdej sprzedaży (historia cen).
36. Rezerwacja: jeden klient, jeden dzień odbioru, pozycje (produkt + ilość w kg); przy kompletowaniu zapisuje się odważoną masę każdej pozycji.
37. Stany rezerwacji: złożona → anulowana (przez klienta do 18:00 dnia poprzedniego, zwalnia ilości w planie dostawy) | przygotowana do odbioru (po skompletowaniu i zważeniu) → odebrana (wydanie i zapłata) | nieodebrana (brak odbioru do 18:00 w dniu odbioru, naliczenie opłaty); anulowana, odebrana, nieodebrana — końcowe. Nowy jest stan „przygotowana do odbioru”.

Nie dopisano (pytanie do Karola): jakie dane personelu przechowuje system (SH podaje m.in. datę zatrudnienia) i czy produkt można wycofać z oferty.

**Napięcie do potwierdzenia:** przykład w notatce 19.10 („100 kg ziemniaków”) przekracza limit 20 kg na rezerwację ustalony przez Karola. W raporcie obowiązuje 20 kg; przykład z notatki nie jest używany.

**Napięcie do potwierdzenia:** notatka 19.10 wyklucza płatności online, a obciążanie karty za nieodebranie jest płatnością kartą na odległość. W raporcie przyjęto, że płatność za towar zostaje w sklepie, a obciążenie karty wykonuje właściciel przez operatora płatności poza systemem. Warto, żeby Karol potwierdził to z prowadzącym.

## Gdzie co jest

| Ścieżka | Zawartość |
|---|---|
| `dokumentacja/sprawozdanie.tex` | całe sprawozdanie: strona tytułowa, spis treści, Specyfikacja projektu (TODO na koniec), rozdz. 1–14 (etap 1 → rozdz. 1, 2.1–2.2 i 3; etap 2 → 2.3–2.5 i 4–7; etap 3 → 8–11; etap 4 → 12; etap 5 → 13–14) |
| `dokumentacja/sprawozdanie.pre-restructure.tex.bak`, `…pre-restructure2.tex.bak` | kopie `sprawozdanie.tex` sprzed pierwszej i drugiej przebudowy 04.11.2026; do usunięcia przez Karola |
| `dokumentacja/figury/` | rysunki do sprawozdania (PDF/PNG + źródła diagramów) |
| `docs/plan-sprawozdania.md` | wzorzec SH, szkielet sprawozdania i tabela pokrycia wytycznych v4 (§1), plan per sekcja (§2), kolejność prac (§3), minimum Django (§4), pytania Q1–Q14 (§5), plan aplikacji i opis systemu (§6), kolejność omawiania etapu 1 (§7) |
| `docs/indeks-zrodel.md` | wszystkie źródła z faktami i stronami PDF (część A) oraz podpunkt raportu → gdzie szukać (część B), lista braków do uzupełnienia przez Karola |
| `materialy/IDB_wytyczne_v4.pdf` | wytyczne prowadzącego — źródło nadrzędne |
| `materialy/notatki/` | notatki z konsultacji (19.10.2026) |
| `materialy/bazdy danych/`, `materialy/io/` | przykładowe raporty i instrukcje (forma, nie fakty) |
| `materialy/formatki_pwr/` | formatki PWr (źródło układu strony tytułowej) |
| `PLAN.md` | dawna kolejka obowiązków z przypisaniem osób; nieaktualna po Q1/Q2, czeka na przebudowę (Q12) |
| `.claude/skills/` | skille agenta (niżej) |
| `.claude/settings.json` | blokada `git commit` / `git push` dla agenta |

## Skille

- `styl-sprawozdania` (`.claude/skills/styl-sprawozdania/SKILL.md`) — logika wywodu (jak jest → dlaczego → co zmienia system), rejestr, zakazane „AI-izmy”, budowa dobrej sekcji, zasada „etap 1 od nowa”, typografia i konwencje LaTeX, samokontrola przed oddaniem sekcji. Obowiązuje przy każdym pisaniu tekstu do sprawozdania.
- `zrodla-sprawozdania` (`.claude/skills/zrodla-sprawozdania/SKILL.md`) — hierarchia źródeł, struktura raportu wg SH, gdzie szukać informacji, wymagane elementy etapów 1–5, checklista kompletności. Obowiązuje przy omawianiu każdej sekcji.

Oba skille i notatka z konsultacji są importowane na końcu tego pliku, więc są zawsze w kontekście. `docs/plan-sprawozdania.md` i `docs/indeks-zrodel.md` są duże — czytaj je na bieżąco, właściwą sekcję.

## Budowanie PDF

```bash
cd dokumentacja
latexmk -pdf -interaction=nonstopmode sprawozdanie.tex   # wynik: sprawozdanie.pdf
latexmk -c                                               # sprzątanie plików pomocniczych
```

Po każdej edycji sprawdź w `sprawozdanie.log`: brak błędów (`grep -n '^!' sprawozdanie.log`), brak `undefined references` i `Overfull \hbox` większych niż kilka pt. Pliki pomocnicze i PDF są w `.gitignore`.

## Kod Django (gdy powstanie)

- Jedna konwencja nazw modeli (PL albo EN — Q11) w całym projekcie i w raporcie.
- Schemat tylko przez migracje Django; dostęp do bazy wyłącznie przez ORM.
- Zmiany stanu (dostawa, sprzedaż, rezerwacja) w `transaction.atomic`; stan nie schodzi poniżej zera.
- Sekrety (`SECRET_KEY`, hasła) poza repozytorium (`.env` jest w `.gitignore`).
- Minimum weryfikacji: `python manage.py check`, `python manage.py test`. Wyniki do raportu tylko z faktycznych uruchomień.
- Docelowy podział aplikacji i kolejność budowy: `docs/plan-sprawozdania.md` §4 i §6.

## Importowane zawsze

Ustalenia z konsultacji 19.10.2026:
@materialy/notatki/notatka_ze_spotkania_19_10_26.md

Zasady stylu:
@.claude/skills/styl-sprawozdania/SKILL.md

Źródła i wymagane elementy:
@.claude/skills/zrodla-sprawozdania/SKILL.md
