# MALL DIN Cash & Carry

Django e-commerce supermarket for **MALL DIN Cash & Carry**, Bhogiwall / Dhobighat, Lahore, Pakistan.

## Stack
- Django 5/6
- SQLite (development) — use PostgreSQL for production
- WhiteNoise for static files
- Ready for Vercel deployment

## Local setup
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py add_images   # optional image URLs
python manage.py createsuperuser
python manage.py runserver
```

## Vercel deployment
1. Connect this GitHub repo to Vercel.
2. Set environment variables in Vercel:
   - `DJANGO_SECRET_KEY` = (generate a strong secret)
   - `DJANGO_DEBUG` = `False`
   - `ALLOWED_HOSTS` = `.vercel.app,your-custom-domain.com`
   - `CSRF_TRUSTED_ORIGINS` = `https://*.vercel.app,https://your-domain.com`
3. Framework: Django (or Other). Vercel detects `manage.py`.
4. Deploy.

**Note:** SQLite is not durable on Vercel (ephemeral filesystem). For real production, switch to Postgres (Neon, Supabase, etc.) via `DATABASE_URL`.

## Features
- Product catalog, categories, search, filters
- Cart (session + logged-in)
- Checkout (COD / Bank / Online)
- Orders history
- User accounts & profile
- Newsletter, About, Contact, Dining, Entertainment pages
