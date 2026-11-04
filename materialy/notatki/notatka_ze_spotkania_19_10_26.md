# Notatka ze spotkania projektowego (konsultacje)

**Data spotkania:** 19.10.2026
**Uczestnicy:** Prowadzący oraz 3-osobowy zespół projektowy  
**Przedmiot:** Przegląd postępów i założeń projektu aplikacji webowej dla lokalnego warzywniaka

\---

## 1\. O czym rozmawiano (przebieg spotkania)

Spotkanie dotyczyło weryfikacji wstępnej koncepcji systemu dla małego, stacjonarnego sklepu z warzywami i owocami. Głównym celem biznesowym aplikacji ma być ograniczenie strat związanych z psuciem się świeżego towaru poprzez umożliwienie klientom wcześniejszej rezerwacji produktów.

Prowadzący i studenci omówili:

* **Zakres funkcjonalny:** Uzgodniono, że samo przeglądanie oferty to za mało – kluczowa jest opcja rezerwacji konkretnych ilości (np. 100 kg ziemniaków) z odbiorem osobistym. Na tym etapie wykluczono dowóz do domu oraz zewnętrzne płatności online (płatność odbywa się na miejscu).
* **Technologię:** Zespół wybrał Django (Python) oraz bazę SQLite. System ma działać na fizycznym komputerze postawionym bezpośrednio w sklepie (bez zewnętrznego hostingu).
* **Podział pracy w zespole:** Przejrzano wstępny podział zadań oraz przygotowaną przez studentów analizę SWOT i harmonogram.

\---

## 2\. Główne uwagi i zalecenia prowadzącego

1. **Baza danych SQLite:** Prowadzący mocno przestrzegł przed używaniem SQLite w aplikacji webowej, ponieważ nie radzi sobie ona dobrze z jednoczesnymi zapisami wielu użytkowników naraz. Zespół zaproponował kolejkowanie zapisów, ale temat pozostał do głębszego przemyślenia.
2. **Nowa rola użytkownika:** Do listy ról (właściciel, sprzedawca, dostawca, klient) należy dopisać **„klienta-obserwatora”** – kogoś, kto przegląda asortyment bez logowania, a konto zakłada dopiero w momencie chęci złożenia rezerwacji.
3. **Dwa różne panele:** Wbudowany panel Django ma być przeznaczony wyłącznie dla sprzedawcy/właściciela. Klienci zewnętrzni muszą otrzymać odrębny, dedykowany interfejs webowy (ze względów bezpieczeństwa i wygody).
4. **Podział ról w grupie:**

   * Na etapie analizy: jeden student powinien wejść w rolę klienta/właściciela sklepu, a dwaj pozostali przeprowadzić z nim wywiad jako analitycy.
   * Na etapie projektowania: zespół powinien pracować wspólnie (burza mózgów), zamiast sztywno rozdzielać zadania na jedną osobę.
   * Ścisły podział (backend, frontend, baza danych) ma sens dopiero przy właściwym kodowaniu (implementacji).
5. **Korekty w analizie SWOT:**

   * Zbyt krótki czas (2 tygodnie zaplanowane na wdrożenie) to **słaba strona** zespołu, a nie zagrożenie zewnętrzne.
   * W zagrożeniach należy umieścić nieprzewidziane błędy techniczne w trakcie kodowania.
   * Zapis „brak kodu na etapie analizy” należy wykreślić ze słabych stron, bo na etapie analizy brak kodu jest całkowicie normalny.
6. **Kwestie formalne do uzupełnienia:**

   * Wpisać konkretne wersje technologii (Django, Python).
   * Zaznaczyć licencje bibliotek (open source) i uwzględnić to w kosztorysie (0 zł za narzędzia).
   * Poprawić sformułowanie: w podejściu *code-first* w Django powstaje „model bazy danych” z klas ORM (reverse engineering), a nie klasyczny „projekt bazy”.
   * W sekcji wdrożenia opisać jasną instrukcję instalacji aplikacji na komputerze stacjonarnym w sklepie.

\---

## 3\. Ustalenia i kolejne kroki (Action Items)

* **Termin:** Zespół ma **1 miesiąc** na formalne zakończenie całej fazy projektowej (wymagania funkcjonalne/niefunkcjonalne, diagram przypadków użycia, diagram klas ORM, poprawiony SWOT i kosztorys).
* **Prace równoległe:** Studenci zadeklarowali, że poza pisaniem dokumentacji zaczną już konfigurować środowisko i przygotowywać prostą, działającą wersję uruchomieniową aplikacji.
* **Stan prac:** Zespół idzie zgodnie z harmonogramem.

