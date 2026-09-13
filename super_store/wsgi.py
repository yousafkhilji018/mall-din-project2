"""
WSGI config for super_store project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'super_store.settings')

application = get_wsgi_application()


def _bootstrap_db():
    """Create tables + seed a few products on Vercel cold start."""
    if not os.environ.get('VERCEL'):
        return
    try:
        from django.core.management import call_command
        call_command('migrate', run_syncdb=True, verbosity=0, interactive=False)
    except Exception:
        return
    try:
        from store.models import Category, Product
        if Product.objects.exists():
            return
        grocery, _ = Category.objects.get_or_create(
            slug='grocery',
            defaults={'name': 'Grocery', 'icon': '🛒', 'sort_order': 1},
        )
        household, _ = Category.objects.get_or_create(
            slug='household',
            defaults={'name': 'Household', 'icon': '🏠', 'sort_order': 2},
        )
        samples = [
            ('National Pure Atta 5kg', 'national-atta-5kg', grocery, 'National', '5kg', 1450, True, True),
            ('Nestle Milkpak 1L', 'nestle-milkpak-1l', grocery, 'Nestle', '1L', 280, True, False),
            ('Surf Excel 1kg', 'surf-excel-1kg', household, 'Surf Excel', '1kg', 520, False, True),
            ('Lifebuoy Soap 3-Pack', 'lifebuoy-soap-3pack', household, 'Lifebuoy', '3 pack', 220, False, False),
            ('Shan Biryani Masala', 'shan-biryani-masala', grocery, 'Shan', '60g', 95, True, True),
            ('Dalda Cooking Oil 1L', 'dalda-oil-1l', grocery, 'Dalda', '1L', 650, False, False),
        ]
        for name, slug, cat, brand, weight, price, featured, best in samples:
            Product.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': name,
                    'category': cat,
                    'description': f'{name} - quality product from MALL DIN Cash & Carry.',
                    'brand': brand,
                    'weight': weight,
                    'price': price,
                    'stock': 50,
                    'is_active': True,
                    'is_featured': featured,
                    'is_bestseller': best,
                    'rating': 4.5,
                },
            )
    except Exception:
        pass


_bootstrap_db()
