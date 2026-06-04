# Rishta App

Backend API for a matrimony platform built with Django and Django REST Framework.

## Tech Stack

- Python
- Django 4
- Django REST Framework
- PostgreSQL
- JWT authentication (`djangorestframework-simplejwt`)
- Stripe payments
- drf-spectacular (OpenAPI/Swagger docs)

## Repository Layout

```text
rishta-app/
├── README.md
└── Rishta_App/
    ├── manage.py
    ├── requirements.txt
    ├── configurations/        # Django settings (common/dev/prod)
    ├── backend/               # Main apps and API endpoints
    │   ├── authentication/    # OTP + auth flows
    │   ├── users/             # User profiles, sentiments, profile views
    │   ├── events/            # Event management
    │   ├── payments/          # Payment plans + Stripe events
    │   ├── notifications/     # Notification models and APIs
    │   ├── swagger/           # API docs endpoints
    │   └── urls.py            # Root URL routing
    ├── templates/             # Email templates (activation, OTP)
    └── services/              # Shared utility services
```

## Getting Started

### 1) Clone and enter project

```bash
git clone https://github.com/Luqman-Ud-Din/rishta-app.git
cd rishta-app/Rishta_App
```

### 2) Create and activate virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Configure environment variables

Create a `.env` file in `Rishta_App/` using `configurations/.env.dist` as a reference.

Required values include:

- `SECRET_KEY`
- `DB_NAME`, `DB_USER_NAME`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`
- `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_PORT`, `EMAIL_USE_TLS`
- `STRIPE_SECRET_KEY`, `STRIPE_PUBLIC_KEY`
- `USER_TRIAL_PERIOD`

### 5) Run migrations

```bash
python manage.py migrate
```

### 6) Start development server

```bash
python manage.py runserver
```

API will be available at `http://127.0.0.1:8000/`.

## API Routes (High Level)

- `/admin/` — Django admin
- `/swagger/` — OpenAPI/Swagger UI
- `/api/` — Authentication, users, events, payments, and notifications endpoints

## Testing

Run tests from `Rishta_App/`:

```bash
python manage.py test
```
