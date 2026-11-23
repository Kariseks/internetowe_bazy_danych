# Plan integracji warzywniaka

Punktem wyjścia jest main po pobraniu zmian (db7728e). Na tym etapie istnieją szablony obu paneli, formularze, projekt SQL i scenariusze testów. Puste modele i usługi zwracające przykładowe dane uniemożliwiają realizację rezerwacji. Gałąź Cursor 257d5cd wnosi mapowanie wytycznych v4 na etapy projektu. Poniższa kolejność uwzględnia decyzję o Django 5.2 i MySQL 8.4.

| Kolejność | Odpowiedzialność w tej integracji | Praca i kryterium zakończenia |
|---|---|---|
| 1 | Koordynacja | Scalić plan Cursor, odczytać notatkę z konsultacji, wykład, oba przykłady SWOT i raporty wzorcowe. Zapisać instrukcje do ponownego użycia w projekcie. |
| 2a | Interfejs | Podłączyć polski i angielski w obu panelach, przełączane style, dostępne formularze i nawigację klawiaturą. Sprawdzić katalog, rezerwację oraz panel personelu. |
| 2b | Baza | Odwzorować encje sklepu w ORM, dodać ograniczenia i migracje. Odtworzyć schemat od zera. |
| 2c | Serwer i integracja | Zastąpić przykładowe odczyty i zapisy operacjami ORM. Sprawdzić izolację kont, historię cen, limity, rozliczenia, odmowę sprzedaży ponad stan i ponowienia operacji. |
| 2d | Analiza i redakcja | Opracować ocenę czynników i macierze SWOT/TOWS zgodnie z wykładem. Uzgodnić scenariusze, instrukcję obsługi i słownik danych z aplikacją. |
| 3 | Baza i dokumentacja | Odczytać tabele i klucze z działającej bazy po migracji. Wstawić wynikowy diagram do raportu. |
| 4 | Integracja i dokumentacja | Uruchomić testy, zarejestrować ich wyniki, odświeżyć ilustracje ekranów i zbudować PDF. Oddzielnie opisać elementy wymagające rzeczywistego wdrożenia w sklepie. |

Podział obowiązków studentów i terminy zaliczenia określa sprawozdanie. Instrukcje redakcyjne są w `zasady.md`, a indeks materiałów w `docs/indeks-zrodel.md`.
