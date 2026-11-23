# Blog Management System

A Django-rendered blog platform with public publishing, user dashboards, post moderation, likes/comments, contact messages, and a staff-only editorial console.

## Requirements
- Python 3.10+ (developed with Python 3.14)
- Django 5.2
- Pillow

## Windows PowerShell setup
Run from the folder containing `manage.py`:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/. The custom staff console is at `/manage/`; Django's protected admin is at `/django-admin/`. Register an ordinary account at `/accounts/register/`. Make an account staff/superuser through Django admin to access the moderation console.

## Features
- Public home, about, searchable/category-filtered paginated listing, published detail pages, related stories, contact form.
- Account registration/login/logout, profile management and validated profile images.
- User dashboard, own-post CRUD, drafts and approval submissions, status/rejection feedback.
- Staff-only dashboard and management of moderation, categories, comments, contact messages, and user activation. Use Django admin for full account add/edit/delete operations.
- Unique per-user likes, comments, and blog/profile images.

## Data relationships
`UserProfile` is one-to-one with Django `User` (deleted with the user). `BlogPost` references its author (cascade delete) and optional `Category` (category deletion sets category to null). Comments and Likes reference both user and post (cascade delete). A database unique constraint prevents duplicate user/post likes. Contact messages are independent records.

## Moderation
Authors can save Draft or submit Pending. Staff can publish or reject pending posts; rejection requires a reason. Public views query only Published posts. Editing a post resubmits it as Pending or saves it as Draft.

## Uploads and deployment
Uploads are limited to valid JPG/PNG/WebP images: 5 MB for blog images and 3 MB for profile photos. Pillow verifies image contents. Local DEBUG mode serves files from `media/`. For production, set a private SECRET_KEY, disable DEBUG, configure ALLOWED_HOSTS, use HTTPS, and configure persistent media storage and static collection/serving. SQLite is suitable for local development; assess a managed database, backups, and operational monitoring before production.

## Checks performed
`python manage.py check` and `python manage.py makemigrations --check --dry-run`. The test suite was not run.
