# Chronova project audit and Django migration plan

## Audit date and scope

This audit covers the complete repository at the start of the Django foundation work. The project is a static Bootstrap prototype; it contains **no PHP files**, PHP includes, Composer metadata, or database connection/query code. Consequently, there is no live PHP application or database schema to translate.

## Existing structure

| Location | What exists | Decision |
| --- | --- | --- |
| `index.html` | Chronova landing page: navbar, hero, four feature cards, footer | Preserve as the original prototype; use as future public landing-page reference. |
| `pages/` | `timetable.html`, `habits.html`, `goals.html`, `ideas.html` | Preserve as future module UI references; do not wire into Part 1. |
| `css/style.css` | Shared Chronova dark gradient, hero, logo, card and responsive styles | Reused in `static/css/style.css`; extended only for authentication/dashboard. |
| `js/script.js` | Browser-only add/remove interactions for future timetable, habits, goals and ideas | Reused in `static/js/script.js`; intentionally not exposed as functional modules yet. |
| `images/logo.png` | Brand logo | Reused in `static/images/logo.png`. |
| `images/hero.png` | Landing-page illustration | Reused in `static/images/hero.png`. |
| `README.md` | Minimal existing file | Preserved. |

## UI layouts and reusable components

The existing reusable visual language is the dark navy/purple gradient background, circular illuminated logo, Bootstrap cards, responsive navbar, hero layout and feature-card grid. There are no PHP partials, template includes, server-side components, database models, sessions, authentication pages or persistence layer.

## Migration plan

1. **Foundation (this delivery):** create the Django project, MySQL environment configuration, authentication, profile, preferences, dashboard shell, admin registrations, migrations and tests.
2. **Template conversion:** keep source prototype pages unchanged, then convert each future feature page to a Django template when its backed model and authorization rules are designed.
3. **Future modules (out of scope):** add attendance, tasks/timetable, habits, goals, ideas, AI planning and analytics as isolated Django apps with migrations and tests.
4. **Deployment:** set production secret/environment variables, disable debug, serve collected static files and use real email delivery before release.

## Reuse versus replacement

**Reuse:** both images, existing CSS styling, JavaScript source, Bootstrap design conventions, page content/labels and the basic navbar/card layout.

**Replace:** static page-to-page links are replaced by namespaced Django URLs where Part 1 has a backing view; client-only identity/state is replaced by Django sessions, CSRF-protected forms, hashed passwords and MySQL models.

**Missing before this work:** Python/Django configuration, a database schema, environment configuration, authentication, passwords/reset emails, profiles, preferences, a dashboard, access control, admin configuration, migrations, tests, server-rendered templates and media handling.

## MySQL setup and connection test

Create the database and least-privilege account in MySQL:

```sql
CREATE DATABASE chronova CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'chronova_user'@'localhost' IDENTIFIED BY 'choose-a-strong-password';
GRANT ALL PRIVILEGES ON chronova.* TO 'chronova_user'@'localhost';
FLUSH PRIVILEGES;
```

Copy `.env.example` to `.env`, enter the same values, then run:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py test_database
python manage.py migrate
python manage.py test
python manage.py createsuperuser
python manage.py runserver
```

`test_database` opens the configured MySQL connection and executes a safe `SELECT 1`. `migrate` creates the Django and Chronova tables. The tests create sample users and associated profile/preference records in Django's isolated test database. Visit `/accounts/register/` or `/admin/` after starting the server.
