---
name: sprawozdanie-ibd
description: Weryfikuje pokrycie etapów projektu sklepu warzywnego w sprawozdaniu według wytycznych IBD v4.
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
