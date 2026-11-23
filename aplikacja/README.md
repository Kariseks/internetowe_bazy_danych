# Uruchomienie sklepu

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

[Katalog klienta](http://127.0.0.1:8000/) jest publiczny. Załóż konto, zaakceptuj zasady i zarejestruj kartę w symulatorze, aby zarezerwować produkt. Wybór PL/EN i przycisk wysokiego kontrastu znajdują się w nagłówku. W [panelu personelu](http://127.0.0.1:8000/admin/) zaloguj się utworzonym kontem właściciela. Przed sprzedażą wpisz faktycznie przyjętą dostawę. Polecenie `asortyment_demo` wypełnia pusty katalog ośmioma produktami, cenami i ilościami na ladę.

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
