# Aplikacja Django

Python 3.12, Django 5.2, MySQL 8.4 w Dockerze. `mysqlclient` wymaga bibliotek klienta MySQL.
    
```bash
cp .env.example .env
uv venv --python 3.12 .venv
source .venv/bin/activate
uv pip install -r requirements.txt

docker compose up -d --wait
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
