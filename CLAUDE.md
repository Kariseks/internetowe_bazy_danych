# CLAUDE.md — sprawozdanie IBD „Lokalny warzywniak”

Główna instrukcja dla Claude Code w tym repozytorium. Jedno źródło prawdy dla agenta: ten plik + skille w `.claude/skills/` + plan i indeks w `docs/`. `README.md` to opis zewnętrzny repozytorium, nie instrukcja dla agenta.

## Projekt

- Przedmiot: Internetowe bazy danych, Politechnika Wrocławska, W4N, kierunek Informatyka techniczna. Prowadzący: dr inż. Roman Ptak.
- Grupa: Karol Gąsior 280913, Mikołaj Winiecki 280952, Mateusz Złośnik 281201. Z agentem pracuje Karol.
- Temat: aplikacja webowa jednego małego, stacjonarnego sklepu warzywnego. Cel biznesowy: mniej strat na psującym się towarze dzięki rezerwacjom konkretnych ilości z odbiorem osobistym. Bez dowozu i płatności online (płatność na miejscu). Poza zakresem bez wyraźnej prośby Karola: wiele sklepów, programy lojalnościowe, aplikacja mobilna, integracja z kasą, „pełny ERP”.
- Stack: Python + Django, baza MySQL (InnoDB, sterownik `mysqlclient`; Q3). Wersje zatwierdzone 04.11.2026 (Q10): Python 3.12, Django 5.2 LTS, MySQL Community Server 8.4 LTS. Maksymalnie wbudowane mechanizmy Django (auth z grupami jako rolami, admin, formularze, ORM i migracje, sesje, CSRF, widoki resetu hasła, backend poczty — SMTP w sklepie, konsola w dev/testach), SQLite najwyżej do lokalnych testów programistów, uruchamiane na komputerze w sklepie, bez hostingu.
- Role: właściciel, sprzedawca (Django Admin), klient z kontem (osobny panel klienta), klient-obserwator (przegląd bez logowania), dostawca (bez konta — dostawy wprowadza personel; decyzja 04.11.2026). Operator płatności (karta klienta) należy do otoczenia systemu.
- Terminy laboratoriów: 19.10 analiza, 17.11 projekt, 30.11 implementacja i wdrożenie, 14.12 prezentacja.
- Produkt pracy: `dokumentacja/sprawozdanie.tex` (jeden plik LaTeX: Specyfikacja projektu + 13 rozdziałów w układzie i logice raportu „Sklep hydrauliczny” — jak jest → dlaczego system → co zmienia → cel i wymagania → uzasadnienie i organizacja (z technikami modelowania w 3.3.1) → PU → baza → implementacja → testy → wdrożenie i podręcznik → prezentacja i zaliczenie → wnioski — przy czym każdy wymóg wytycznych v4 i notatki 19.10 ma własny nagłówek; szkielet, „Wzorzec SH” i tabela pokrycia w `docs/plan-sprawozdania.md` §1). Kodu aplikacji jeszcze nie ma.

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
| Q3 | SQLite czy MySQL | **Rozstrzygnięte 04.11.2026 przez Karola: MySQL** (zastępuje wcześniejszą tego dnia decyzję agenta „SQLite”). Powody: zalecenie W4 pkt 7 (Python + MySQL) i brak potrzeby uzasadniania współbieżności SQLite (N19 uwaga 1). Silnik InnoDB, sterownik `mysqlclient`. Wersja MySQL Community Server 8.4 LTS zatwierdzona przez Karola 04.11.2026 (Q10). Współbieżność (3.3.2, do napisania): blokady wierszy InnoDB, rezerwacja w jednej transakcji z `select_for_update` na planie dostawy (sprawdzenie puli + zapis pozycji). SQLite najwyżej do lokalnych testów programistów. Szczegóły: plan §5 Q3. |
| Q4 | Zestaw technik modelowania (UML + ERD + normalizacja) | **Rozstrzygnięte 04.11.2026 (Karol):** UML (przypadki użycia, czynności, klasy, stany) + ERD; rozdział „Techniki modelowania” usunięty — techniki i narzędzie w 3.3.1 (z uzasadnieniem pominięcia DHF/DNF/DFE), struktura funkcjonalna we wstępie rozdz. 4, informacyjna we wstępie rozdz. 6. Graf stanów rezerwacji (6.7) **zostaje** (Karol, 04.11.2026). |
| Q5 | Notacja ERD i narzędzie diagramów | **Rozstrzygnięte 04.11.2026 (Karol):** Visual Paradigm **Community Edition** (bez numeru wersji), wszystkie diagramy UML i ERD. Notacja ERD: **Crow's Foot** — tak jak modele bazy danych w „Sklepie hydraulicznym” (rozdz. 5, s. 55–65: tabele z PK/FK, zakończenia linii `|`, `o<`, `|<`); materiały IO nie mają ERD, tylko diagramy UML z VP. Wpisane w 3.3.1 i we wstępie rozdz. 6. |
| Q6 | Komputer w sklepie, dostęp klientów (LAN / internet) | **Rozstrzygnięte 04.11.2026 (Karol zatwierdził propozycję agenta, pkt 71):** dostęp przez przeglądarkę do serwera Django na komputerze w sklepie (WN4); mini PC (np. Intel N100, 16 GB RAM, SSD 512 GB), Ubuntu Server 24.04 LTS, Nginx (HTTPS, statyczne, `/admin/` tylko z LAN) + Gunicorn (WSGI), Let's Encrypt przez Certbot, porty 80/443 i ewentualnie dynamiczny DNS, `cron` (18:00, 6:00, `mysqldump`). Tekst w 3.3.1. Pozostałe elementy WN z pkt 55 nadal do akceptacji. |
| Q7 | Reguły rezerwacji, rola dostawcy | **Rozstrzygnięte 04.11.2026** — szczegóły pod tabelą. Opis słowny i parametry skalowalne napisane w `sprawozdanie.tex`. |
| — | Szkielet etapu 1 | **Zatwierdzone 04.11.2026:** „Grupa projektowa i podział obowiązków” przeniesiona tuż przed „Harmonogram”; dodano „Parametry skalowalne” pod „Opis słowny systemu”. Reszta szkieletu bez zmian (Q12). |
| — | Dostawca | **Rozstrzygnięte 04.11.2026:** dostawca nie ma konta w systemie; jego dostawy wprowadza personel (osoba otwierająca sklep). Dostawca nie jest aktorem systemu, tylko elementem otoczenia. |
| — | Operator płatności | **Rozstrzygnięte 04.11.2026:** operator płatności (rejestracja i obciążanie karty klienta) należy do otoczenia systemu. Opisane w 1.4 „Interesariusze i otoczenie systemu” (04.11.2026). |
| — | Przebudowa struktury | **Zrobione 04.11.2026 na prośbę Karola:** układ rozdziałów, nazwy i podział na wzór raportu „Sklep hydrauliczny” (`materialy/bazdy danych/`), przy zachowaniu wszystkich wymagań wytycznych v4 i uwag z notatki 19.10. Zachowano: „Grupa projektowa i podział obowiązków” tuż przed „Harmonogram”, „Parametry skalowalne”, P1–P8. Napisany tekst i `\label{}` przeniesione bez zmian. Kopia sprzed przebudowy: `dokumentacja/sprawozdanie.pre-restructure.tex.bak` (Karol może ją usunąć). Szkielet i tabela pokrycia: plan §1. |
| — | Osobne nagłówki dla wymogów wytycznych | **Zrobione 04.11.2026 na prośbę Karola:** każdy element W4 i N19 ma własny, rozpoznawalny nagłówek. Dodano: 2.2 Zakres projektu (wydzielony z celu), 3.3.1 Wybór technologii, wersje i licencje, 3.3.2 Współbieżne zapisy w bazie SQLite (po Q3 przemianowane na „…w bazie MySQL (InnoDB)”), 3.6.1 Skład grupy, 3.6.2 Podział obowiązków w etapach projektu, rozdz. 4 Techniki modelowania (4.1, 4.2; **usunięty 04.11.2026**, patrz Q4), 6.5 Diagramy czynności wybranych PU (Q4; po przenumerowaniu 5.5), 7.1 Podejście code-first, 8.2 Środowisko programistyczne i repozytorium kodu, 8.4 Oddzielenie kodu od HTML – szablony Django, 13.1 Plan prezentacji, 13.2 Materiały przekazywane do zaliczenia. Przemianowano wg brzmienia wytycznych: rozdz. 1 „Opis słowny świata rzeczywistego”, 1.4 „…otoczenie podsystemu”, rozdz. 3 „Uzasadnienie potrzeby realizacji…”, 3.3 „Techniczna wykonalność systemu”, 3.4 „Koszt wytworzenia systemu (kosztorys)”, 7.3 „Model konceptualny (ERD)”, 7.6 „Słownik danych (definicje obiektów)”, 8.3 „Architektura trójwarstwowa”, 8.7 „Model fizyczny bazy danych”, rozdz. 12 „Wdrożenie aplikacji…”, 12.1.1–12.1.2 „…w sklepie”, rozdz. 13 „Prezentacja i zaliczenie projektu”. Tekst i etykiety bez zmian. Mapa: plan §1 „Pokrycie wymagań”. |
| — | Otoczenie systemu (1.4) | **Rozstrzygnięte 04.11.2026 (najprostsze warianty):** (1) zapłata za towar przy ladzie (gotówka lub terminal kartowy) poza systemem — system nie zapisuje płatności za sprzedaż, rozlicza tylko opłatę 10% za nieodebranie przez operatora płatności; (2) dostawca bez konta, w otoczeniu jako źródło dostaw wprowadzanych przez personel; (3) kasa fiskalna to osobne urządzenie bez integracji. Sekcja 1.4 napisana (`sec:otoczenie`, `tab:otoczenie`). |
| — | Druga przebudowa struktury | **Zrobione 04.11.2026 na prośbę Karola:** układ jeszcze ściślej wg SH. Rozdz. 1: 1.1 Obecny sposób działania sklepu (jak jest, `sec:opis`) → 1.2 Problemy P1–P8 (`sec:problemy`) → 1.3 Proponowany system (co wprowadza i zmienia, nowa `sec:system`) → 1.4 Interesariusze i otoczenie → 1.5 Parametry skalowalne. Rozdz. 2 „Cel projektu oraz wymagania systemu” (jak SH 2); SWOT…harmonogram w rozdz. 3 „Uzasadnienie i organizacja projektu”; architektura w 7.2 „Struktura systemu” (jak SH 6.1.2). Dawny „Opis słowny” rozdzielony na 1.1 i 1.3 bez utraty treści; dopisano zdania przejścia, odwołania w P1 i P5 wskazują teraz `sec:system`. Kopia: `dokumentacja/sprawozdanie.pre-restructure2.tex.bak` (Karol może usunąć). |
| Q8 | Wersje minimalna / standardowa / rozszerzona | **Zaproponowane przez agenta 04.11.2026, do akceptacji Karola** (pkt 56): minimalna = konta, katalog, plan dostawy, rezerwacje z wszystkimi warunkami, wydanie, oznaczanie nieodebranych z opłatą; standardowa = ewidencja (dostawa, sprzedaż, ubytki, stan, zestawienie zamówienia), stan „przygotowana”, zmiana rezerwacji, zaległości i blokada; rozszerzona = zestawienia właściciela, panel klienta na telefonach, karta przez testowe środowisko operatora. Tekst w 2.5. |
| — | Rozdział 2 | **Napisany 04.11.2026 na prośbę Karola** (po przejściu na MySQL): 2.1 cel z „Uwagą”, 2.2 zakres, 2.3.1–2.3.8 WF1–WF48 (po dopisaniu WF 04.11.2026) (etykiety `wf:…` w `\item`, odwołania przez `\ref`), 2.4 WN1–WN11 (`wn:…`), 2.5 wersje. Uzupełnienia agenta: pkt 38–56. |
| Q9 | Koszt wytworzenia (praca, sprzęt) | **Rozstrzygnięte 04.11.2026 (Karol): kwoty zatwierdzone bez zmian** — 40 zł/h, 210 h = 8 400 zł; mini PC 2 000 zł, UPS 400 zł, dysk 250 zł; utrzymanie 190 zł/rok; razem 11 050 zł. Tekst w 3.4 (`tab:koszt`). |
| — | Rozdziały 4–5 | **Napisane 04.11.2026 na prośbę Karola:** 4.1 aktorzy (`tab:aktorzy`), 4.2 PU1–PU31 (`tab:pu`) ze związkami i 4 miejscami na diagramy modułów; 5.1–5.5 scenariusze 11 PU w układzie SH, 5.6 dwa miejsca na diagramy czynności. Uzupełnienia agenta: pkt 72–77. Otwarte: makiety ekranów, ponowna rejestracja karty. |
| — | Rozdział 3 | **Napisany 04.11.2026 na prośbę Karola:** 3.1 SWOT (`tab:swot`), 3.2 CSF (`tab:csf`), 3.3 wykonalność (3.3.1 `tab:technologie`, notacja Crow's Foot; 3.3.2 InnoDB, `select_for_update`), 3.4 kosztorys, 3.5 plan, 3.6 skład i podział (`tab:sklad`, `tab:obowiazki`), 3.7 harmonogram (`tab:harmonogram`, sprawdzony z terminami zajęć). Uzupełnienia agenta: pkt 62–70. |
| Q10 | Wersje Pythona i Django | **Rozstrzygnięte 04.11.2026 (Karol):** Python 3.12, Django 5.2 LTS, MySQL Community Server 8.4 LTS. Wpisane w WN2 i komentarzu 3.3.1. |
| — | Odpowiedzi Karola do rozdz. 2 | **04.11.2026:** (1) dostęp przez serwer aplikacji Django, jak najwięcej wbudowanych mechanizmów Django (nowe WN3); (2) reset hasła e-mailem (widoki Django, WF reset hasła — wersja minimalna) i wysyłka e-mail: powiadomienia o koncie, rezerwacjach i opłatach (std), przypomnienie w dniu odbioru (rozsz.); SMTP (nowe WN); serwer poczty dopisany do otoczenia w 1.4; (3) wersje jak Q10; (4) dane personelu tylko z modelu `User` Django: login, imię, nazwisko, e-mail, skrót hasła, rola (grupa), aktywność — bez PESEL, adresu, telefonu (WF4). Otwarte: czy symulowaną rejestrację karty potwierdzić z prowadzącym (zostaje jak jest). |
| Q11 | Nazewnictwo modeli PL/EN, sposób liczenia stanu | **Zaproponowane przez agenta 04.11.2026, do akceptacji (pkt 80–81):** nazwy polskie bez znaków diakrytycznych (`Meta.db_table`), stan produktu i zaległość liczone, nie przechowywane. Tekst w 6.1 i 6.4, DDL w `baza/schema.sql`. |
| — | Rozdział 6 i `baza/` | **Napisane 04.11.2026 na prośbę Karola:** 6.1 code-first, 6.2 encje (`tab:encje`) i związki (`tab:zwiazki`), 6.3–6.5 miejsca na ERD i diagram klas, 6.4 normalizacja, 6.6 słownik danych (`tab:slownik`, 74 atrybuty generowane z tej samej listy co DDL), 6.7 graf stanów; `baza/schema.sql` i `baza/README.md`. Uzupełnienia agenta: pkt 80–86. |
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

### Rozdz. 2 (cel, zakres, WF, WN, wersje) — uzupełnione przez agenta — do akceptacji Karola

Od Karola (04.11.2026): treść „Uwagi” w 2.1 (bez dowozu, bez płatności online za towar, bez integracji z kasą, dostawca bez konta), MVP z rezerwacjami, MySQL. Reszta poniżej to propozycje agenta.

38. 2.1: cel w trzech akapitach z odwołaniami do P1–P8; w „Uwadze” dopisano też wyłączenia z `CLAUDE.md` (wiele sklepów, program lojalnościowy, aplikacja mobilna).
39. 2.2: zakres prac (analiza → wdrożenie z instrukcją i podręcznikiem) i pięć obszarów funkcji: katalog i konta, rezerwacje i plan dostawy, ewidencja, rozliczenia, administracja.
40. Każde konto ma dokładnie jedną rolę; musi istnieć co najmniej jedno aktywne konto właściciela; konta personelu tylko dezaktywuje się (bez usuwania); właściciel może dezaktywować konto klienta (rezerwacje i zaległość zostają) (WF2–WF4, WF7, WF25).
41. Konto bez zarejestrowanej karty nie może składać rezerwacji (WF5).
42. ~~Logowanie adresem e-mail (unikalnym) dla wszystkich ról, także personelu; hasło ≥ 8 znaków wg standardowych walidatorów Django; bez uwierzytelniania dwuskładnikowego i bez resetu hasła przez e-mail w żadnej wersji (WF8–WF11).~~ **Zmienione przez Karola 04.11.2026:** reset hasła e-mailem (widoki Django) dodany jako WF; login z modelu `User` Django — personel ma login nadany przez właściciela, klient ma login równy adresowi e-mail (oba unikalne). Do akceptacji zostaje: hasło ≥ 8 znaków wg walidatorów Django, bez 2FA, link resetu ważny 3 dni (domyślnie w Django).
43. Nowa funkcja: rejestracja ubytku (towar wyrzucony), obniża stan — potrzebna do pomiaru strat z P3 (WF14).
44. Zestawienie zamówienia na następny dzień z planu dostawy, dostępne dla sprzedawcy (WF16).
45. Wyszukiwanie klienta po nazwisku, e-mailu lub telefonie przez personel (WF20).
46. Wycofanie produktu z oferty bez usuwania z historii (WF22) — wcześniej otwarte pytanie.
47. Wynik obciążenia karty: skuteczne zmniejsza zaległość o pobraną kwotę, nieudane jej nie zmienia (WF26).
48. Zestawienia właściciela za okres: sprzedaż i ubytki według produktów, różnice plan–dostawa, liczba i wartość nieodebranych rezerwacji (WF27).
49. Nowa funkcja: zmiana pozycji rezerwacji do 18:00 dnia poprzedzającego dzień odbioru, na tych samych warunkach (WF29); rozdz. 1 mówił tylko o anulowaniu.
50. Ilości w rezerwacji z dokładnością do 0,1 kg; klient widzi orientacyjną wartość wg cen bieżących (WF28).
51. Klient może zmienić tylko numer telefonu; e-mail (identyfikator) bez zmiany (WF35).
52. Katalog oznacza dzień, dla którego przyjmowanie rezerwacji się zakończyło, jako niedostępny (WF36).
53. Warunki przyjęcia rezerwacji zebrane w WF39, w tym „brak innej niezakończonej rezerwacji na ten dzień”; sprawdzenie i zapis w jednej transakcji.
54. Oznaczenie „nieodebrana” dotyczy rezerwacji złożonych i przygotowanych, wykonywane przez system po 18:00; opłata zaokrąglana do 1 gr (WF43).
55. WN1–WN11: utf8mb4; katalog i panel klienta z internetu przez HTTPS, panel administratora tylko z sieci lokalnej (Q6); komputer pracuje całą dobę; ≤ 2 s na katalog i zapis rezerwacji przy 2 + 20 użytkownikach; baza na ≥ 5 lat (ok. 2 mln wierszy wg wartości docelowych z `tab:parametry`); masy 0,01 kg, kwoty 1 gr, strefa Europe/Warsaw; skróty haseł, CSRF; kopia codziennie po zamknięciu, poza komputerem, odtworzenie ≤ 1 h; Chrome/Firefox/Edge aktualne, personel ≥ 1280 px, telefony od 360 px dopiero w wersji rozszerzonej. **Zmienione 04.11.2026:** wersje zatwierdzone przez Karola (Q10); dostęp przez serwer Django potwierdzony (Q6, częściowo); reszta nadal do akceptacji.
56. Podział na wersje (Q8), w tym: w wersji minimalnej i standardowej rejestracja karty symulowana (formularz zwraca testowy identyfikator), w rozszerzonej testowe środowisko operatora; oznaczanie nieodebranych z opłatą już w minimalnej, blokada i rozliczenia w standardowej.

57. Treść powiadomień e-mail (WF): potwierdzenie założenia konta; potwierdzenie złożenia, zmiany i anulowania rezerwacji (dzień odbioru, pozycje); informacja o naliczonej opłacie i o blokadzie — wersja standardowa. Przypomnienie o 6:00 w dniu odbioru (godzina zamknięcia, wysokość opłaty) — wersja rozszerzona.
58. Wysyłka przez serwer SMTP skrzynki pocztowej sklepu; w dev i testach backend konsolowy Django (nowe WN). Serwer poczty e-mail dopisany do otoczenia w `tab:otoczenie` (1.4); klient otrzymuje wiadomości e-mail.
59. Dane klienta spoza `User` (telefon, identyfikator karty, zaległość) w osobnym modelu powiązanym z kontem (WN3).

60. ~~3.3.1: Visual Paradigm w wydaniu Community Edition; numer wersji `% TODO`.~~ **Rozstrzygnięte 04.11.2026 (Karol):** Community Edition, bez numeru wersji (TODO usunięte); notacja ERD Crow's Foot (Q5).
61. Zdania o strukturze funkcjonalnej (wstęp rozdz. 4, z odwołaniem do WF) i informacyjnej (wstęp rozdz. 6) oraz uzasadnienie pominięcia DHF/DNF/DFE (3.3.1).

### Rozdz. 3 (SWOT, CSF, wykonalność, kosztorys, plan, grupa, harmonogram) — uzupełnione przez agenta — do akceptacji Karola

62. SWOT (`tab:swot`): mocne — wąski zakres, wbudowane mechanizmy Django, reguły zapisane jako WF, znajomość VP z IO i bezpłatne narzędzia; słabe — 13 dni od 17.11 do 30.11, brak doświadczenia z wdrożeniem, MySQL i HTTPS, zmiana SQLite → MySQL, równoległa praca nad dokumentacją i kodem; szanse — mniejsze nadwyżki (P3), katalog przyciąga klientów (P5), historia sprzedaży i ubytków, późniejsze rozszerzenia; zagrożenia — błędy techniczne, awaria komputera w sklepie, klienci nie korzystają lub nie odbierają, zmiana wymagań i rozrost zakresu. Wniosek: prosta działająca wersja równolegle z projektem.
63. CSF (`tab:csf`): pula nieprzekroczona (test dwóch jednoczesnych rezerwacji), stan ≥ 0 i zgodny z ewidencją, czas lokalny 18:00, rejestracja sprzedaży trzech produktów ≤ 30 s (liczba wymyślona przez agenta), wersja minimalna w sklepie do 30.11, odtworzenie kopii na innym komputerze. **Zatwierdzone 04.11.2026 (Karol), łącznie z progiem 30 s.**
64. Tabela technologii (`tab:technologie`). **Licencje sprawdzone przez agenta 04.11.2026** (PyPI, docs.python.org, pliki LICENSE/COPYING w repozytoriach, latex-project.org): Python PSF License v2, Django BSD-3-Clause, MySQL 8.4 Community GPLv2, mysqlclient **GPL-2.0-or-later** (poprawione z GPLv2), Git GPLv2, LaTeX LPPL; dodano Ubuntu Server 24.04 LTS, Gunicorn (MIT), Nginx (BSD-2-Clause), Certbot (Apache-2.0). VP CE bezpłatna do użytku niekomercyjnego.
65. Treść 3.3.2: blokady wierszy InnoDB, spójny odczyt, `transaction.atomic` + `select_for_update` na planie dostawy (rezerwacja) i na stanie produktu (sprzedaż, ubytek), krótkie transakcje, wycofanie i ponowienie przy przekroczeniu czasu blokady lub zakleszczeniu.
66. Kosztorys (Q9, `tab:koszt`): stawka 40 zł/h; godziny 30 + 45 + 90 + 15 + 30 = 210 h (8 400 zł); mini PC 2 000 zł, UPS 400 zł, dysk zewnętrzny 250 zł (2 650 zł); domena 60 zł/rok, Let's Encrypt 0 zł, energia ok. 130 kWh = 130 zł/rok (15 W × 24 h, ok. 1 zł/kWh), hosting 0 zł; razem 11 050 zł; prowizja operatora płatności pominięta. Wszystkie kwoty są szacunkami agenta, nie cenami z ofert. **Zatwierdzone 04.11.2026 (Karol).**
67. Plan projektu (3.5): pięć etapów wytycznych z odwołaniami do rozdziałów.
68. Skład grupy i obszary (`tab:sklad`, zmienione 04.11.2026 razem z pkt 69): Karol — koordynacja, dokumentacja, model bazy, serwer w sklepie; Mikołaj — wymagania, logika rezerwacji, ewidencji i rozliczeń, testy jednostkowe, kopia zapasowa; Mateusz — przypadki użycia, panel klienta, admin, testy akceptacyjne, podręcznik.
69. Podział w etapach (`tab:obowiazki`) — **przebudowany 04.11.2026 na prośbę Karola**: kolumny „Prowadzi” i „Wspiera”, 24 zadania; prowadzi Karol 8, Mikołaj 8, Mateusz 7 (+ pokaz wspólnie), łączny udział 14–15 zadań na osobę. **Rola właściciela w wywiadzie — Mateusz Złośnik — zatwierdzona przez Karola, TODO usunięte.** Reszta podziału do akceptacji.
70. Harmonogram (`tab:harmonogram`): daty pośrednie 10.11 (środowisko, modele, prosta wersja) i 24.11 (wersja minimalna) z planu w plan §6.8; terminy zajęć 19.10, 17.11, 30.11, 14.12 sprawdzone (17.11 = 29 dni po 19.10, 30.11 = 13 dni po 17.11).
71. Q6 — sprzęt i serwery (3.3.1, `tab:technologie`): mini PC z procesorem np. Intel N100, 16 GB RAM, SSD 512 GB, ok. 15 W; Ubuntu Server 24.04 LTS (wsparcie do 2029); Nginx + Gunicorn; Let's Encrypt + Certbot; porty 80/443 na routerze, dynamiczny DNS przy zmiennym IP; `/admin/` tylko z LAN; `cron`: 18:00 nieodebrane, 6:00 przypomnienia, kopia `mysqldump` na dysk zewnętrzny. Etykiety `wn:wdrozenie`, `wn:kopia` dodane do WN. **Zatwierdzone 04.11.2026 (Karol).**

### Rozdz. 4–5 (aktorzy, lista PU, scenariusze) — uzupełnione przez agenta — częściowo zatwierdzone

72. Aktorzy (`tab:aktorzy`): klient-obserwator (każdy przed zalogowaniem, także personel), użytkownik zalogowany (abstrakcyjny: klient, sprzedawca), właściciel jako specjalizacja sprzedawcy, Czas, operator płatności, serwer poczty; dostawca nie jest aktorem.
73. Lista PU1–PU31 (`tab:pu`, numeracja przez `\pu{…}` i `\ref`; od 04.11.2026 z PU13 „Zarejestruj kartę płatniczą”, kolejne numery przesunięte o 1), cztery moduły: Konta użytkowników, Rezerwacje, Magazyn i sprzedaż, Rozliczenia; zamknięcie o 18:00 bez osobnego PU. **Zatwierdzone 04.11.2026 (Karol).**
74. Związki (numeracja po dodaniu PU13): PU21 Wydaj «include» PU22 Wyszukaj klienta i PU15 Sprzedaż; «extend»: PU9, PU10 → PU11; PU20 → PU19; PU23 → PU22; PU4 → PU3; PU2 → PU1; PU13 → PU7.
75. Scenariusze 11 PU (5.1–5.5): Załóż konto, Zaloguj się, Zresetuj hasło, Złóż rezerwację, Anuluj rezerwację, Przyjęcie dostawy, Sprzedaż, Przygotuj rezerwację, Wydaj rezerwację, Ustal plan dostawy, Oznacz nieodebrane. Szczegóły dopisane przez agenta: po założeniu konta komunikat i formularz logowania (bez automatycznego logowania); konto zostaje bez karty, gdy rejestracja karty się nie uda; ten sam komunikat przy resecie dla nieznanego adresu (zachowanie Django); A2 w dostawie — wyróżnienie produktu, gdy dostarczono mniej niż zarezerwowano; przygotowanie z masą mniejszą niż zarezerwowana (także 0 kg); wydanie nieprzygotowanej rezerwacji z ważeniem przy kliencie; brak zmiany planu dnia już zamkniętego; opłata zapisana mimo nieudanej wysyłki e-mail. **Zatwierdzone 04.11.2026 (Karol pozostawił szczegóły agentowi).**
76. Nowy podrozdział 5.5 „Przypadki użycia uruchamiane przez czas”; diagramy czynności w 5.6 (`sec:czynnosci`) — dla PU8 i PU21. Miejsca na rysunki: makra `\diagramvp` i `\ekran` (schemat nazw plików niżej, „Rysunki — schemat nazw plików”); 11 diagramów i 14 ekranów.
77. Nowe etykiety WF (bez zmiany numeracji): `wf:role`, `wf:konto-wlasciciela`, `wf:konta-sprzedawcow`, `wf:karta`, `wf:dezaktywacja-klienta`, `wf:login`, `wf:logowanie`, `wf:panel-admina`, `wf:dostawa`, `wf:ubytek`, `wf:stan`, `wf:cena`, `wf:zmiana-hasla`, `wf:zalozenie-konta`.
78. **Ponowna rejestracja karty — decyzja Karola 04.11.2026:** klient może dołączyć albo ponownie dołączyć kartę po nieudanej próbie. Dodano: WF `wf:karta-ponowna` (w „Funkcje dostępne dla klienta”, po `wf:zaleglosc`; kolejne numery WF przesunięte o 1, odwołania przez `\ref`), PU13 „Zarejestruj kartę płatniczą” (`pu:karta`, «extend» PU7) ze scenariuszem w 5.2, odnośniki w PU2 A2 i PU8 A1, wersja minimalna w 2.5, aktorzy (klient, operator płatności), diagram modułu Konta. Szczegóły agenta (do akceptacji): klient może też zastąpić kartę nową — nowy identyfikator w miejsce poprzedniego; nieudana rejestracja zostawia dotychczasowy stan konta.
79. Ekrany (14 miejsc w rozdz. 5, makro `\ekran`): zawartość ekranu dopisana przez agenta przy każdym rysunku, z odwołaniem do kroków scenariusza.

### Rozdz. 6 i `baza/schema.sql` (model bazy danych) — uzupełnione przez agenta — do akceptacji Karola

80. Q11 (propozycja): nazwy tabel i atrybutów polskie bez znaków diakrytycznych (`pozycja_rezerwacji`), modele Django z `Meta.db_table`; tabele `auth_user`, `auth_group`, `auth_user_groups` z Django bez zmian; tabele techniczne Django (sesje, migracje) poza modelem.
81. Q11 (propozycja): stanu produktu i zaległości klienta nie przechowuje się — liczone z dostaw, sprzedaży i ubytków oraz z opłat i skutecznych rozliczeń; przy sprzedaży i ubytku blokada wiersza produktu (3.3.2 i PU15 przeredagowane). Furtka: atrybuty z bieżącą wartością, jeśli sumy okażą się zbyt wolne.
82. Encje (15 tabel): profil_klienta (PK = FK konta), produkt, cena_produktu (historia cen od dnia), plan_dostawy (wiersz tworzony przy pierwszej zmianie planu lub rezerwacji, wcześniej plan = standardowa ilość), dostawa (jedna dziennie), pozycja_dostawy, ubytek, rezerwacja (z `oplata_za_nieodebranie` i kolumną wyliczaną `aktywny_klient_id` dla jednej niezakończonej rezerwacji na dzień), pozycja_rezerwacji (`masa_odwazona_kg`), sprzedaz (`rezerwacja_id` UNIQUE dla wydania), pozycja_sprzedazy (cena z chwili sprzedaży), rozliczenie_zaleglosci (wpłata albo obciążenie, `skuteczne`).
83. Typy i ograniczenia: BIGINT dla tabel aplikacji, INT dla `auth_*` (jak w Django 5.2); masy DECIMAL z 0,01 kg (pozycja rezerwacji 0,1 kg, ≤ 20), kwoty DECIMAL(…,2); CHECK na ilościach, cenach, stanach i opłacie; klucze obce bez akcji kaskadowych; sortowanie `utf8mb4_pl_0900_ai_ci`; indeksy: `rezerwacja(dzien_odbioru, stan)`, daty sprzedaży, ubytków i rozliczeń, telefon klienta.
84. Związki i liczności (`tab:zwiazki`), normalizacja do 3NF z uzasadnieniem pozornych powtórzeń (cena w pozycji sprzedaży, opłata, kolumna wyliczana), reguły pilnowane przez aplikację (20 kg, pula, plan ≥ zarezerwowane, 18:00, jedna rola).
85. Graf stanów (6.7): przejścia z PU, w tym złożona → odebrana przy wydaniu nieprzygotowanej rezerwacji (PU21 A1); po anulowaniu można złożyć nową rezerwację na ten sam dzień, jeśli zapisy trwają.
86. `baza/schema.sql` sprawdzony tylko parserem (sqlglot, dialekt MySQL) — brak serwera MySQL na tym komputerze; uruchomić na MySQL 8.4 przed oddaniem. `baza/README.md`: wg strony porównania wydań VP funkcje „Generate ERD from database” i „Generate & reverse DDL” są prawdopodobnie niedostępne w Community Edition — zalecone ręczne narysowanie ERD w VP CE, alternatywy: wydanie z Database engineering (np. wersja próbna Standard) albo kontrola w MySQL Workbench.

### Rysunki — schemat nazw plików

Wszystkie rysunki w `dokumentacja/rysunki/`, format PNG, nazwy małymi literami, bez znaków diakrytycznych, słowa rozdzielone `-`. Makra w `sprawozdanie.tex` wstawiają plik, gdy istnieje; do tego czasu rysują ramkę „TODO: brak pliku” z oczekiwaną ścieżką i zawartością rysunku.

- Diagramy z Visual Paradigm — `dokumentacja/rysunki/diagramy/<rodzaj>-<obiekt>.png`, makro `\diagramvp{etykieta}{podpis}{nazwa}{zawartość}`. Rodzaje: `pu` (`pu-aktorzy`, `pu-modul-konta`, `pu-modul-rezerwacje`, `pu-modul-magazyn`, `pu-modul-rozliczenia`), `czynnosci` (`czynnosci-pu08-zlozenie-rezerwacji`, `czynnosci-pu21-wydanie-rezerwacji`), `erd` (`erd-konceptualny`, `erd-logiczny`), `klasy` (`klasy-modele-orm`), `stany` (`stany-rezerwacja`).
- Ekrany aplikacji (makiety albo zrzuty) — `dokumentacja/rysunki/ekrany/puNN-<opis>.png`, makro `\ekran{etykieta}{podpis}{nazwa}{zawartość}`; `NN` = dwucyfrowy numer PU z `tab:pu`. Obecne: `pu02-zalozenie-konta`, `pu03-logowanie`, `pu04-reset-hasla`, `pu04-nowe-haslo`, `pu08-rezerwacja`, `pu10-anulowanie`, `pu11-moje-rezerwacje`, `pu13-rejestracja-karty`, `pu14-przyjecie-dostawy`, `pu15-sprzedaz`, `pu19-rezerwacje-na-dzien`, `pu20-przygotowanie-rezerwacji`, `pu21-wydanie-rezerwacji`, `pu26-plan-dostawy`.
- Po zmianie numeracji PU zmienić nazwy plików ekranów i diagramów czynności (`grep -n 'ekran{\|diagramvp{' dokumentacja/sprawozdanie.tex`).

**Napięcie do potwierdzenia:** przykład w notatce 19.10 („100 kg ziemniaków”) przekracza limit 20 kg na rezerwację ustalony przez Karola. W raporcie obowiązuje 20 kg; przykład z notatki nie jest używany.

**Napięcie do potwierdzenia:** notatka 19.10 wyklucza płatności online, a obciążanie karty za nieodebranie jest płatnością kartą na odległość. W raporcie przyjęto, że płatność za towar zostaje w sklepie, a obciążenie karty wykonuje właściciel przez operatora płatności poza systemem. Warto, żeby Karol potwierdził to z prowadzącym.

## Gdzie co jest

| Ścieżka | Zawartość |
|---|---|
| `dokumentacja/sprawozdanie.tex` | całe sprawozdanie: strona tytułowa, spis treści, Specyfikacja projektu (TODO na koniec), rozdz. 1–13 (etap 1 → rozdz. 1, 2.1–2.2 i 3; etap 2 → 2.3–2.5 i 4–6; etap 3 → 7–10; etap 4 → 11; etap 5 → 12–13) |
| `dokumentacja/sprawozdanie.pre-restructure.tex.bak`, `…pre-restructure2.tex.bak` | kopie `sprawozdanie.tex` sprzed pierwszej i drugiej przebudowy 04.11.2026; do usunięcia przez Karola |
| `dokumentacja/figury/` | dawny katalog rysunków (makro `\figura`) |
| `dokumentacja/rysunki/diagramy/`, `dokumentacja/rysunki/ekrany/` | rysunki wg schematu nazw (sekcja „Rysunki — schemat nazw plików”) |
| `baza/schema.sql`, `baza/README.md` | DDL modelu bazy (MySQL 8.4) i instrukcja ERD w Visual Paradigm |
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
- Zmiany stanu (dostawa, sprzedaż, rezerwacja) w `transaction.atomic` z `select_for_update` na blokowanych wierszach (MySQL/InnoDB); stan nie schodzi poniżej zera.
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
