from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from .models import Product, Category, Cart, CartItem, Order, OrderItem, Newsletter
from .forms import CartAddForm, CheckoutForm, NewsletterForm


class _EmptyCart:
    def get_item_count(self):
        return 0
    def get_total(self):
        return 0
    @property
    def items(self):
        class _QS:
            def select_related(self, *a, **k):
                return self
            def all(self):
                return []
            def exists(self):
                return False
            def delete(self):
                pass
        return _QS()


def get_cart(request):
    try:
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            cart, _ = Cart.objects.get_or_create(session_key=session_key)
        return cart
    except Exception:
        return _EmptyCart()


def home_view(request):
    featured_products, bestsellers, categories, cart_item_count = [], [], [], 0
    try:
        featured_products = list(Product.objects.filter(is_active=True, is_featured=True)[:8])
        bestsellers = list(Product.objects.filter(is_active=True, is_bestseller=True)[:8])
        categories = list(Category.objects.filter(parent__isnull=True)[:8])
        cart_item_count = get_cart(request).get_item_count()
    except Exception:
        pass
    return render(request, 'home.html', {
        'featured_products': featured_products,
        'bestsellers': bestsellers,
        'categories': categories,
        'cart_item_count': cart_item_count,
    })


def products_view(request):
    products_list = []
    categories = []
    all_categories = []
    query = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')
    price_min = request.GET.get('price_min', '')
    price_max = request.GET.get('price_max', '')
    sort = request.GET.get('sort', '')
    tab = request.GET.get('tab', '')
    try:
        products = Product.objects.filter(is_active=True)
        categories = list(Category.objects.filter(parent__isnull=True))
        all_categories = list(Category.objects.all())
        if query:
            products = products.filter(
                Q(name__icontains=query) | Q(description__icontains=query) |
                Q(brand__icontains=query) | Q(category__name__icontains=query)
            )
        if category_slug:
            products = products.filter(
                Q(category__slug=category_slug) | Q(category__parent__slug=category_slug)
            )
        if price_min:
            try:
                products = products.filter(price__gte=float(price_min))
            except ValueError:
                pass
        if price_max:
            try:
                products = products.filter(price__lte=float(price_max))
            except ValueError:
                pass
        if tab == 'bestsellers':
            products = products.filter(is_bestseller=True)
        elif tab == 'new':
            products = products.filter(is_new_arrival=True)
        elif tab == 'deals':
            products = products.filter(discount_percent__gt=0)
        if sort == 'price_low':
            products = products.order_by('price')
        elif sort == 'price_high':
            products = products.order_by('-price')
        elif sort == 'newest':
            products = products.order_by('-created_at')
        elif sort == 'rating':
            products = products.order_by('-rating')
        elif sort == 'popular':
            products = products.order_by('-is_bestseller', '-rating')
        else:
            products = products.order_by('-created_at')
        page_obj = Paginator(products, 12).get_page(request.GET.get('page'))
    except Exception:
        page_obj = []
    return render(request, 'store/products.html', {
        'products': page_obj,
        'categories': categories,
        'all_categories': all_categories,
        'query': query,
        'selected_category': category_slug,
        'price_min': price_min,
        'price_max': price_max,
        'sort': sort,
        'tab': tab,
        'cart_item_count': get_cart(request).get_item_count(),
    })


def product_detail_view(request, slug):
    try:
        product = get_object_or_404(Product, slug=slug, is_active=True)
        related_products = list(
            Product.objects.filter(category=product.category, is_active=True).exclude(id=product.id)[:4]
        )
    except Exception:
        messages.error(request, 'Product not found.')
        return redirect('products')
    return render(request, 'store/product_detail.html', {
        'product': product,
        'related_products': related_products,
        'cart_form': CartAddForm(),
        'cart_item_count': get_cart(request).get_item_count(),
    })


def categories_view(request):
    try:
        categories = list(Category.objects.filter(parent__isnull=True))
    except Exception:
        categories = []
    return render(request, 'store/categories.html', {
        'categories': categories,
        'cart_item_count': get_cart(request).get_item_count(),
    })


def category_products_view(request, slug):
    try:
        category = get_object_or_404(Category, slug=slug)
        products = Product.objects.filter(
            Q(category=category) | Q(category__parent=category), is_active=True
        )
        sort = request.GET.get('sort', '')
        if sort == 'price_low':
            products = products.order_by('price')
        elif sort == 'price_high':
            products = products.order_by('-price')
        elif sort == 'newest':
            products = products.order_by('-created_at')
        elif sort == 'rating':
            products = products.order_by('-rating')
        page_obj = Paginator(products, 12).get_page(request.GET.get('page'))
    except Exception:
        messages.error(request, 'Category not found.')
        return redirect('products')
    return render(request, 'store/category_products.html', {
        'category': category,
        'products': page_obj,
        'sort': request.GET.get('sort', ''),
        'cart_item_count': get_cart(request).get_item_count(),
    })


def add_to_cart_view(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id, is_active=True)
    except Exception:
        messages.error(request, 'Product not found.')
        return redirect('products')
    cart = get_cart(request)
    if isinstance(cart, _EmptyCart):
        messages.error(request, 'Cart unavailable. Please try again.')
        return redirect('products')
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
        except (ValueError, TypeError):
            quantity = 1
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity = min(cart_item.quantity + quantity, max(product.stock, 1))
            cart_item.save()
        elif quantity > product.stock and product.stock > 0:
            cart_item.quantity = product.stock
            cart_item.save()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'cart_count': cart.get_item_count(),
                'message': f'{product.name} added to cart!',
            })
        messages.success(request, f'{product.name} added to cart.')
    return redirect('products')


def remove_from_cart_view(request, item_id):
    try:
        cart_item = get_object_or_404(CartItem, id=item_id)
        name = cart_item.product.name
        cart_item.delete()
        messages.success(request, f'{name} removed from cart.')
    except Exception:
        messages.error(request, 'Item not found.')
    return redirect('cart')


def update_cart_view(request, item_id):
    try:
        cart_item = get_object_or_404(CartItem, id=item_id)
        if request.method == 'POST':
            quantity = int(request.POST.get('quantity', 1))
            quantity = max(1, min(quantity, max(cart_item.product.stock, 1)))
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated.')
    except Exception:
        messages.error(request, 'Could not update cart.')
    return redirect('cart')


def cart_view(request):
    cart = get_cart(request)
    try:
        cart_items = list(cart.items.select_related('product').all()) if not isinstance(cart, _EmptyCart) else []
        cart_total = cart.get_total()
    except Exception:
        cart_items, cart_total = [], 0
    delivery_fee = 200
    return render(request, 'store/cart.html', {
        'cart': cart,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'delivery_fee': delivery_fee,
        'grand_total': cart_total + delivery_fee,
        'cart_item_count': cart.get_item_count(),
    })


@login_required
def checkout_view(request):
    cart = get_cart(request)
    try:
        cart_items = list(cart.items.select_related('product').all()) if not isinstance(cart, _EmptyCart) else []
    except Exception:
        cart_items = []
    if not cart_items:
        messages.warning(request, 'Your cart is empty.')
        return redirect('products')
    cart_total = cart.get_total()
    delivery_fee = 200
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                full_name=form.cleaned_data['full_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                area=form.cleaned_data.get('area', ''),
                city=form.cleaned_data.get('city', 'Lahore'),
                payment_method=form.cleaned_data.get('payment_method', 'cod'),
                total_amount=cart_total + delivery_fee,
                delivery_fee=delivery_fee,
            )
            for item in cart_items:
                OrderItem.objects.create(
                    order=order, product=item.product,
                    quantity=item.quantity, price=item.product.price,
                )
                item.product.stock = max(0, item.product.stock - item.quantity)
                item.product.save()
            CartItem.objects.filter(cart=cart).delete()
            messages.success(request, 'Order placed successfully!')
            return redirect('order_confirmation', order_id=order.id)
    else:
        form = CheckoutForm(initial={
            'full_name': f'{request.user.first_name} {request.user.last_name}'.strip(),
            'email': request.user.email,
            'city': 'Lahore',
        })
    return render(request, 'store/checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'delivery_fee': delivery_fee,
        'grand_total': cart_total + delivery_fee,
        'cart_item_count': cart.get_item_count(),
    })


@login_required
def order_confirmation_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_confirmation.html', {
        'order': order,
        'cart_item_count': get_cart(request).get_item_count(),
    })


@login_required
def order_history_view(request):
    try:
        orders = list(Order.objects.filter(user=request.user))
    except Exception:
        orders = []
    return render(request, 'store/order_history.html', {
        'orders': orders,
        'cart_item_count': get_cart(request).get_item_count(),
    })


def newsletter_view(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            try:
                _, created = Newsletter.objects.get_or_create(email=form.cleaned_data['email'])
                messages.success(request, 'Subscribed!' if created else 'Already subscribed.')
            except Exception:
                messages.error(request, 'Could not subscribe right now.')
        else:
            messages.error(request, 'Invalid email.')
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def search_view(request):
    query = request.GET.get('q', '')
    try:
        products = Product.objects.filter(is_active=True)
        if query:
            products = products.filter(
                Q(name__icontains=query) | Q(description__icontains=query) |
                Q(brand__icontains=query) | Q(category__name__icontains=query)
            )
        page_obj = Paginator(products, 12).get_page(request.GET.get('page'))
    except Exception:
        page_obj = []
    return render(request, 'store/search_results.html', {
        'products': page_obj,
        'query': query,
        'cart_item_count': get_cart(request).get_item_count(),
    })
