# Chronova Part 2 — implementation guide

## New application structure

```
website/       public marketing pages: home, features, about, contact
tasks/         categories and complete task lifecycle
timetable/     weekly/day schedule entries
attendance/    subjects and dated attendance records
templates/     reusable base plus page templates per app
static/css/    Chronova visual tokens and form support
static/js/     navigation, modals, reveals, counters and schedule toggles
```

## Created or modified files

| Area | Files | Purpose |
| --- | --- | --- |
| Project routing | `chronova/settings.py`, `chronova/urls.py` | Registers the Part 2 apps and their namespaced URL routes. |
| Public website | `website/apps.py`, `website/views.py`, `website/urls.py`, `templates/website/*` | Serves the public landing, features, about and contact pages. |
| Tasks | `tasks/models.py`, `forms.py`, `views.py`, `urls.py`, `admin.py`, `migrations/0001_initial.py`, `templates/tasks/*` | Implements per-user categories and CRUD tasks with priority, due date and completion state. |
| Timetable | `timetable/models.py`, `forms.py`, `views.py`, `urls.py`, `admin.py`, `migrations/0001_initial.py`, `templates/timetable/*` | Implements per-user weekly entries, validation, edit/delete, week/day views. |
| Attendance | `attendance/models.py`, `forms.py`, `views.py`, `urls.py`, `admin.py`, `migrations/0001_initial.py`, `templates/attendance/*` | Implements subjects, dated present/absent records, percentages and target warnings. |
| Dashboard | `dashboard/views.py`, `templates/dashboard/home.html` | Adds live task, timetable and attendance summaries. |
| Shared presentation | `templates/base.html`, `static/css/chronova.css`, `static/css/forms.css`, `static/js/chronova.js` | Establishes the global identity, responsive navigation, cards, forms, modals, animation and accessibility-aware motion behavior. |

## Design system

The design uses a near-black base (`#090b18`), cyan action color (`#64e3e7`), violet depth color (`#9d8cff`), Manrope display/body typography and DM Mono labels. Reusable elements include `button`, `workspace-card`, `metric-card`, `feature-card`, `modal`, `app-alert`, `eyebrow`, and form styling.

## Animation and responsiveness

The single small JavaScript file manages the mobile menu, accessible modal state, alert dismissal, confirmation prompts, scroll-reveal animation, counter animation, and timetable switching. CSS handles hover elevation, floating panels, a slow orbit, animated pulse bars, responsive grid breakpoints, and disables nonessential motion when the browser requests reduced motion.

## Required terminal commands

The existing `.venv` currently points to a removed/unavailable Python 3.11 executable. Rebuild it using Python 3.12+ before running the project:

```powershell
deactivate
Remove-Item -Recurse -Force .venv
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py check
python manage.py test
python manage.py runserver
```

If `py -3.12` is unavailable, install Python 3.12 or choose the installed 3.12+ interpreter in VS Code, then use `python -m venv .venv`.
