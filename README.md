# MALL DIN Cash & Carry

**Premium supermarket e-commerce** for MALL DIN Cash & Carry  
📍 Bhogiwall / Dhobighat, Lahore, Pakistan

Django-based full-stack online store with product catalog, cart, checkout, user accounts, and static pages (Dining, Entertainment, About, Contact).

---

## Tech Stack

| Layer        | Technology                          |
|--------------|-------------------------------------|
| Backend      | Django 5 / 6                        |
| Database     | SQLite (dev) → Postgres (prod)      |
| Static files | WhiteNoise                          |
| Frontend     | Django templates + custom CSS/JS    |
| Deploy       | Vercel (Python runtime)             |

---

## Features

- **Catalog**: Categories, subcategories, search, filters, sort, pagination
- **Products**: Featured, bestsellers, new arrivals, discounts, ratings, stock
- **Cart**: Session-based (guest) + user-linked cart
- **Checkout**: Cash on Delivery / Bank Transfer / Online Payment
- **Orders**: Order confirmation + order history
- **Accounts**: Register, login, profile, avatar
- **Pages**: About, Contact, Stores, Dining, Entertainment
- **Newsletter** subscription
- **Admin** panel for products, categories, orders

---

## Local Setup

```bash
# 1. Clone
git clone https://github.com/yousafkhilji018/mall-din-project2.git
cd mall-din-project2

# 2. Virtual environment
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 3. Install
pip install -r requirements.txt

# 4. Database
python manage.py migrate
python manage.py seed_data         # 130+ products
python manage.py add_images        # Unsplash image URLs (optional)

# 5. Superuser (optional)
python manage.py createsuperuser

# 6. Run
python manage.py runserver
```

Open: http://127.0.0.1:8000

---

## Vercel Deployment

1. Go to [vercel.com](https://vercel.com) → **Add New Project**
2. Import this GitHub repo: `yousafkhilji018/mall-din-project2`
3. Framework Preset: **Django** (or Other) — Vercel auto-detects `manage.py`
4. Add **Environment Variables**:

| Variable               | Value / Example                          |
|------------------------|------------------------------------------|
| `DJANGO_SECRET_KEY`    | (generate strong random key)             |
| `DJANGO_DEBUG`         | `False`                                  |
| `ALLOWED_HOSTS`        | `.vercel.app,yourdomain.com`             |
| `CSRF_TRUSTED_ORIGINS` | `https://*.vercel.app,https://yourdomain.com` |

5. Deploy

> **Note:** SQLite is **not durable** on Vercel (ephemeral filesystem).  
> For production use Neon / Supabase / Railway Postgres and set `DATABASE_URL`.

---

## Project Structure

```
mall-din-project2/
├── manage.py
├── requirements.txt
├── README.md
├── PROJECT_PLAN.md
├── super_store/          # Project settings, urls, wsgi
├── store/                # Products, cart, orders, seed
├── accounts/             # Auth & profile
├── pages/                # About, Contact, Dining, etc.
├── templates/            # Base + home
├── static/               # CSS + JS
│   ├── css/style.css
│   ├── css/auth.css
│   └── js/main.js
└── media/                # Uploaded images (gitignored)
```

---

## Useful Commands

```bash
python manage.py seed_data      # Load categories + products
python manage.py add_images     # Attach image URLs
python manage.py collectstatic  # For production static
python manage.py createsuperuser
```

---

## License

Private project for MALL DIN Cash & Carry.
