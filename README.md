# Aurum Luxe

A modern responsive luxury e-commerce website built with Django, HTML5, CSS3, JavaScript, and SQLite for development.

## Run Locally

```powershell
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Database

Development uses SQLite in `db.sqlite3`. The app keeps database access behind Django models, so PostgreSQL can be added later by swapping `DATABASES` in `luxecommerce/settings.py` and installing a PostgreSQL driver such as `psycopg2-binary`.
