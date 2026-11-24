# Uruchomienie sklepu

## Szybki pokaz na Ubuntu

Na komputerze prowadzącym pokaz potrzebujesz Pythona 3.12 z modułem venv (pakiet Ubuntu `python3.12-venv`) oraz internetu przy pierwszym pobieraniu bibliotek. Z głównego katalogu projektu wykonaj:

```bash
./aplikacja/przygotuj-demo.sh
./aplikacja/start-demo.sh --wlasciciel
./aplikacja/start-demo.sh
```

Drugie polecenie zakłada konto personelu i pyta o dane logowania. Wykonaj je raz, jeżeli chcesz pokazać panel administratora. Otwórz `http://127.0.0.1:8000/` na komputerze z serwerem. Zatrzymaj go klawiszami Ctrl+C. Kolejne uruchomienia wymagają tylko skryptu startowego. Demonstracja zapisuje dane SQLite i klucz sesji w prywatnym katalogu `aplikacja/.demo/`. Kalafior kosztuje 6,50 zł za sztukę. Pozostałe przykładowe produkty są sprzedawane na wagę. Podczas dodawania produktu właściciel wybiera jednostkę sprzedaży. Limit 20 kg dotyczy towarów ważonych, a liczbę sztuk ogranicza dostępność produktu. Rejestracja karty używa symulatora, a wiadomości pojawiają się w terminalu.

### Połączenie z innego komputera w tej samej sieci

1. Podłącz oba komputery do tej samej zaufanej sieci Wi-Fi lub Ethernet. Na serwerze wpisz `ip -br -4 addr`. Z wiersza aktywnego interfejsu Wi-Fi lub Ethernet odczytaj adres IPv4, np. `192.168.1.24/24`.
2. Zatrzymaj poprzedni serwer. Uruchom `./aplikacja/start-demo.sh 192.168.1.24`, podstawiając własny adres bez końcówki `/24`. Skrypt nasłuchuje na tym interfejsie i dodaje jego adres do listy hostów Django.
3. Na drugim komputerze otwórz w przeglądarce `http://192.168.1.24:8000/` z tym samym adresem. Pod `/admin/` zalogujesz się kontem utworzonym na serwerze. Dane obu paneli zapisują się na komputerze prowadzącym pokaz.
4. Jeśli przeglądarka czeka na połączenie, sprawdź najpierw ten sam adres na serwerze. Przy aktywnej zaporze UFW zezwól na TCP 8000 z adresu drugiego komputera, np. `sudo ufw allow from 192.168.1.35 to any port 8000 proto tcp`. Podstaw adres klienta. Po pokazie usuń regułę poleceniem `sudo ufw delete allow from 192.168.1.35 to any port 8000 proto tcp`. Sieć gościnna z izolacją urządzeń wymaga przełączenia obu komputerów do sieci umożliwiającej połączenia między nimi.

Pokaz korzysta z HTTP i kont demonstracyjnych. Wystarczy port 8000 w sieci lokalnej. Docelową instalację sklepu z HTTPS i MySQL opisuje rozdział o wdrożeniu.

## Instalacja z MySQL

W katalogu `aplikacja` przygotuj Pythona 3.12. Na Ubuntu budowa sterownika MySQL wymaga pakietów `build-essential`, `pkg-config`, `python3-dev` i `default-libmysqlclient-dev`. Do uruchomienia lokalnej bazy MySQL 8.4 potrzebny jest Docker z Compose.

```bash
python3.12 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
cp -n .env.example .env
chmod 600 .env
```

W pliku `.env` ustaw własny losowy klucz Django oraz osobne hasła administratora i użytkownika bazy. Serwer deweloperski obsługuje lokalne adresy wymienione w `DJANGO_ALLOWED_HOSTS`.

```bash
docker compose up -d --wait
python manage.py migrate
python manage.py asortyment_demo
python manage.py createsuperuser
python manage.py runserver
```

[Katalog klienta](http://127.0.0.1:8000/) jest publiczny. Załóż konto, zaakceptuj zasady i zarejestruj kartę w symulatorze, aby zarezerwować produkt. Wybór PL/EN i przycisk wysokiego kontrastu znajdują się w nagłówku. W [panelu personelu](http://127.0.0.1:8000/admin/) zaloguj się utworzonym kontem właściciela. Przed sprzedażą wpisz faktycznie przyjętą dostawę. Polecenie `asortyment_demo` wypełnia pusty katalog dziewięcioma produktami, cenami i ilościami na ladę.

## Próba lokalna bez usługi MySQL

Do demonstracji lub testów ustaw `DB_ENGINE=sqlite` w środowisku przed uruchomieniem migracji, importem asortymentu i startem serwera. Dane zapiszą się w `db.sqlite3`. Wariant ten umożliwia instalację samych zależności Django, python-dotenv i stripe w wersjach podanych w `requirements.txt`.

## Testy i polecenia okresowe

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

Testy tworzą osobną bazę. Dwa scenariusze równoległego zapisu wymagają MySQL z blokadami wierszy. Konta i dane z bazy demonstracyjnej pozostają do dalszej pracy.

O 06:00 czasu sklepu harmonogram systemowy powinien uruchamiać `python manage.py wyslij_przypomnienia`, a o 18:00 oraz po przerwie w pracy serwera `python manage.py oznacz_nieodebrane`. Drugie polecenie rozlicza zaległe odbiory i może zostać bezpiecznie ponowione. Lokalnie wiadomości trafiają na konsolę. Aby dostarczać je pocztą, skonfiguruj `EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` i `DEFAULT_FROM_EMAIL`.

Rejestracja karty domyślnie działa w symulatorze. Opcjonalny klucz środowiska testowego Stripe w `STRIPE_SECRET_KEY` włącza przekierowanie do operatora. Sprzedawca ewidencjonuje płatność za towar przy ladzie. Instrukcje dla komputera sklepowego, kopii bezpieczeństwa i odbioru instalacji zawiera rozdział o wdrożeniu w sprawozdaniu.
