---
name: sprawozdanie-ibd
description: Pomaga pisać i poprawiać sprawozdanie IBD o warzywniaku. Stosuj przy redakcji rozdziałów, obliczaniu SWOT/TOWS i sprawdzaniu zgodności opisu z aplikacją oraz materiałami prowadzącego.
---

# Weryfikacja zakresu sprawozdania

Źródłem wymagań przedmiotu jest materialy/IDB_wytyczne_v4.pdf. Otwórz dokumentacja/sprawozdanie.tex i porównaj zakres wybranego etapu z poniższą tabelą.

| Etap | Elementy do sprawdzenia |
|---|---|
| Analiza (pkt 2–4) | Opis świata rzeczywistego, otoczenie, cel, problemy, SWOT i czynniki sukcesu. Podział prac, plan i harmonogram. Osobno koszt pracy, narzędzi i sprzętu. |
| Projekt (pkt 5, 7–9) | Modele funkcjonalne i informacyjne, aktorzy, scenariusze, diagramy czynności, encje, klucze i słownik. Uzasadnienie wyboru technologii i trzech warstw. |
| Implementacja i walidacja | Powiąż wymagania z widokami, usługami i modelami Django. Odtwórz schemat z bazy po migracjach. W tabelach testów oddziel oczekiwanie od wyniku uzyskanego przy uruchomieniu. |
| Wdrożenie | Instrukcja uruchomienia na komputerze w sklepie, konfiguracja dostępu, dane początkowe i odtworzenie kopii bazy. |
| Prezentacja (pkt 6) | Scenariusz pokazu, role prezentujących, działająca aplikacja, dokumentacja i wnioski. |

Sprawdź metodę analizy w wykładzie nr 1 oraz dwóch przykładach SWOT. Raport sklepu hydraulicznego w materiałach służy jako wzorzec szczegółowości scenariuszy i słownika. Ustalenia sklepu oraz wybrane technologie pochodzą z bieżącego projektu. Zastosuj zasady.md przy redakcji, zbuduj PDF z dokumentacja/sprawozdanie.tex i sprawdź odwołania do rysunków, tabel i sekcji.

## Pisanie rozdziału

Zacznij od decyzji czytelnika. W rozdziale o wdrożeniu sprzedawca ma uruchomić sklep, a w rozdziale o bazie prowadzący ma móc prześledzić zapis rezerwacji. Dobierz do tego jeden rzeczywisty przykład, odpowiedni ekran, tabelę albo relację. Oddziel założenia projektu, stan implementacji i wynik próby. Dla wyniku podaj środowisko, operację oraz obserwowany skutek. Używaj nazw ról i stanów widocznych w aplikacji.

Porównaj wymagania kursu z ustaleniami w `materialy/notatki/notatka_ze_spotkania_19_10_26.md`. Uwzględnij klienta-obserwatora, osobne panele i równoczesny zapis. Przykład dla sklepu: dwóch klientów wybiera ostatnią dostępną ilość. Pokaż regułę dostępności, transakcję MySQL i wynik próby. Powiąż cel ograniczenia strat z pomiarem masy ubytków w sklepie.

## SWOT i TOWS

1. Odczytaj slajdy 29–35 z `materialy/IBD_wyklad_2026_nr1.pdf` i tabele w obu plikach `materialy/Analiza_SWOT_*.docx`. Określ granicę projektu. Zgodnie z konsultacją krótki termin wdrożenia wpisz do W, a nieprzewidziane błędy techniczne do T. Każdy czynnik opisz skutkiem dla tego sklepu.
2. W każdej z grup S, W, O, T rozdziel wagę 1,00. Uzasadnij priorytety. Zachowaj przyjętą skalę ocen i podaj jej znaczenie. W raporcie sklepu wykorzystano skalę 0–2 obecną w przykładzie salonu.
3. Odpowiedz osobno na cztery pytania ze slajdu 33 i cztery ze slajdu 34. Dla przykładu oceń, czy wspólny plan pozwala wykorzystać wcześniejsze deklaracje klientów, a następnie czy takie deklaracje zwiększają wartość planu. Oba kierunki wymagają własnej oceny.
4. Dla każdego wiersza i każdej kolumny pokaż wagę, sumę ocen, iloczyn i rangę. Przy remisie nadaj jednakową rangę. Sprawdź, czy suma ocen wierszy równa się sumie ocen kolumn. Do zestawienia wpisz sumę obu osi oraz sumę ich iloczynów. Dodaj wyniki SWOT i TOWS dla każdej z czterech strategii. Wyjaśnij konsekwencję najlepszego wyniku dla harmonogramu. Przy małej różnicy sprawdź, czy zmiana jednej oceny odwraca kolejność.

## Dostępność w aplikacji i raporcie

Przeprowadź próbę od katalogu do rezerwacji i anulowania. W formularzu wpisz niedostępną ilość. Sprawdź, czy użytkownik rozpoznaje pole, jednostkę, błąd i sposób poprawy. Uwzględnij nawigację bez myszy, powrót fokusu po zamknięciu menu, odczyt komunikatów czytnikiem, kontrast, wąski ekran, działanie bez CSS i JS oraz polskie i angielskie etykiety. Porównaj z wymaganiem `wn:dostepnosc` i instrukcjami w `CLAUDE.md`. W panelu personelu sprawdź analogicznie ważenie i wydanie paczki.

Do tabeli wyników wpisz zadanie, rolę, przeglądarkę i narzędzie z wersją, datę oraz wynik. Opisz dokładny krok, na którym użytkownik napotkał trudność. Jeżeli próba czeka na stanowisko sklepu lub użytkownika, wpisz ją do listy odbiorowej. Przed oddaniem przebuduj PDF i porównaj podpisy z ilustracjami oraz liczby z końcowym logiem testów.
