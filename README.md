# Chronova

Chronova is a Django student productivity platform for task management, attendance, timetables, study planning, assignment deadlines, viva preparation, and career roadmaps.

## Local setup

1. Create and activate a Python 3.14 virtual environment.
2. Install dependencies: `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and set the MySQL credentials and a strong `DJANGO_SECRET_KEY`.
4. Create the MySQL database with UTF-8 support.
5. Run `python manage.py makemigrations` and `python manage.py migrate`.
6. Start the app with `python manage.py runserver`.

## Quality checks

Run `python manage.py check` for Django configuration errors and `python manage.py test` for the test suite. Before a release, run `python manage.py collectstatic --noinput` and confirm authenticated flows using a non-production account.

## Deployment

Set `DJANGO_DEBUG=False`, a unique secret key, explicit `DJANGO_ALLOWED_HOSTS`, secure database credentials, HTTPS at the reverse proxy, and serve collected static files from the web server or object storage. Run migrations as part of the release step and take a database backup beforehand.

## Planning studio

The `/planner/` workspace uses deterministic, transparent plan-generation rules as a reliable first release. The generator functions in `planner/services.py` are intentionally isolated so an approved AI provider can replace them later without changing the data model or UI.
