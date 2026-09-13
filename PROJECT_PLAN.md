# MALL DIN Cash & Carry — Project Plan

## 1. Overview

Online supermarket platform for **MALL DIN Cash & Carry** (Bhogiwall / Dhobighat, Lahore).  
Customers can browse groceries, household, personal care, and home & kitchen products, add to cart, and place orders (COD / Bank / Online).

**Goal:** Simple, fast, mobile-friendly e-commerce that matches local shopping habits (PKR pricing, COD, Lahore delivery).

---

## 2. Scope

### In scope
- Product catalog with categories & subcategories
- Search, filter (price, category), sort
- Guest + logged-in cart
- Checkout & order placement
- User registration / login / profile
- Order history
- Static pages: About, Contact, Stores, Dining, Entertainment
- Newsletter
- Django Admin for staff

### Out of scope (v1)
- Real payment gateway integration (placeholders only)
- Real-time inventory sync with physical store
- Multi-branch stock
- Delivery tracking / rider app
- Native mobile apps

---

## 3. Architecture

```
Browser  →  Django Templates + CSS/JS
                ↓
         Django Views / Forms
                ↓
         Models (Product, Cart, Order…)
                ↓
         SQLite (dev) / PostgreSQL (prod)
```

- **Serverless deploy target:** Vercel (Python runtime + WhiteNoise)
- **Auth:** Django built-in User + custom UserProfile
- **Media:** ImageField + fallback `image_url` (Unsplash for seed)

---

## 4. Apps & Models

| App       | Responsibility                          | Key models                  |
|-----------|-----------------------------------------|-----------------------------|
| `store`   | Catalog, cart, orders, newsletter       | Category, Product, Cart, CartItem, Order, OrderItem, Newsletter |
| `accounts`| Auth & profile                          | UserProfile                 |
| `pages`   | Marketing / info pages                  | (views only)                |
| `super_store` | Settings, root URLs, context processors | —                        |

---

## 5. Key User Flows

1. **Browse** → Home / Store / Category → Product detail  
2. **Add to cart** (AJAX or form) → Cart page → Update qty / remove  
3. **Checkout** (login required) → Address + payment method → Order confirmation  
4. **Account** → Register / Login → Profile / Order history  
5. **Admin** → Manage products, categories, orders, newsletter

---

## 6. Data Seed

- 4 main categories: Grocery, Household, Personal Care, Home & Kitchen  
- 30+ subcategories  
- 130+ products with realistic PKR prices, brands (National, Shan, Nestle, etc.), discounts, ratings  
- Command: `python manage.py seed_data`  
- Optional images: `python manage.py add_images`

---

## 7. Deployment Plan

| Stage        | Action                                      |
|--------------|---------------------------------------------|
| Local        | SQLite + `runserver`                        |
| Preview      | Push to GitHub → Vercel preview deployment  |
| Production   | Vercel production + env vars + Postgres     |

**Environment variables (Vercel):**
- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG=False`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- (later) `DATABASE_URL`

---

## 8. Roadmap (future)

- [ ] PostgreSQL + `dj-database-url`
- [ ] Real payment (JazzCash / EasyPaisa / Stripe)
- [ ] WhatsApp order notifications
- [ ] Delivery fee by area
- [ ] Wishlist persistence
- [ ] Product reviews
- [ ] Admin dashboard charts
- [ ] Multi-language (Urdu) support

---

## 9. Contact / Store Info

- **Store:** MALL DIN Cash & Carry  
- **Location:** Dhobighat / Bhogiwall, Lahore  
- **Phone:** +92 344 1628127  
- **Email:** Abdullah@malldin.com  

---

*Last updated: September 2026*
