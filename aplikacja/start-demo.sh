#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
if [[ ! -x .venv/bin/python || ! -s .demo/klucz ]]; then
    echo "Najpierw uruchom przygotuj-demo.sh." >&2
    exit 1
fi
if (( $# > 1 )); then
    echo "Użycie: $0 [adres-IPv4-serwera | --wlasciciel]" >&2
    exit 2
fi
umask 077
adres=${1:-127.0.0.1}
export DB_ENGINE=sqlite SQLITE_PATH="$PWD/.demo/sklep.sqlite3"
export DJANGO_DEBUG=0 STRIPE_SECRET_KEY='' EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DJANGO_SECRET_KEY=$(<.demo/klucz)
export DJANGO_SECRET_KEY
if [[ "$adres" != --wlasciciel ]]; then
    .venv/bin/python - "$adres" <<'PY'
from ipaddress import IPv4Address
import sys
try:
    adres = IPv4Address(sys.argv[1])
    if adres.is_unspecified or adres.is_multicast or adres.is_reserved:
        raise ValueError
except ValueError:
    sys.exit("Podaj adres IPv4 interfejsu komputera, na którym działa sklep.")
PY
fi
export DJANGO_ALLOWED_HOSTS="localhost,127.0.0.1,$adres"
.venv/bin/python manage.py migrate --noinput
if [[ "$adres" == --wlasciciel ]]; then
    exec .venv/bin/python manage.py createsuperuser
fi
.venv/bin/python manage.py asortyment_demo --dodaj-sztuki
echo "Katalog: http://$adres:8000/   Personel: http://$adres:8000/admin/"
exec .venv/bin/python manage.py runserver --insecure --noreload "$adres:8000"
