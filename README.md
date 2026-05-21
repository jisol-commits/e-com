# Neo China

A modern responsive premium PC components e-commerce website built with Django, HTML5, CSS3, JavaScript, and SQLite for development.

## Run Locally

```powershell
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Chatbot API Key

The store chatbot works with local fallback answers by default. To enable the online AI response endpoint, set your API key before starting Django:

```powershell
$env:OPENAI_API_KEY="your_api_key_here"
python manage.py runserver
```

Optionally set `OPENAI_MODEL`; otherwise the app uses `gpt-5`.

## Database

Development uses SQLite in `db.sqlite3`. The app keeps database access behind Django models, so PostgreSQL can be added later by swapping `DATABASES` in `luxecommerce/settings.py` and installing a PostgreSQL driver such as `psycopg2-binary`.
