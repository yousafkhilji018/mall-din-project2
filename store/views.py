from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from .models import Product, Category, Cart, CartItem, Order, OrderItem, Newsletter
from .forms import CartAddForm, CheckoutForm, NewsletterForm


def get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart


def home_view(request):
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    bestsellers = Product.objects.filter(is_active=True, is_bestseller=True)[:8]
    categories = Category.objects.filter(parent__isnull=True)[:8]
    cart = get_cart(request)
    cart_item_count = cart.get_item_count()

    context = {
        'featured_products': featured_products,
        'bestsellers': bestsellers,
        'categories': categories,
        'cart_item_count': cart_item_count,
    }
    return render(request, 'home.html', context)


def products_view(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.filter(parent__isnull=True)
    all_categories = Category.objects.all()
    query = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')
    price_min = request.GET.get('price_min', '')
    price_max = request.GET.get('price_max', '')
    sort = request.GET.get('sort', '')
    tab = request.GET.get('tab', '')

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(brand__icontains=query) |
            Q(category__name__icontains=query)
        )

    if category_slug:
        products = products.filter(
            Q(category__slug=category_slug) |
            Q(category__parent__slug=category_slug)
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

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    cart = get_cart(request)
    cart_item_count = cart.get_item_count()

    context = {
        'products': page_obj,
        'categories': categories,
        'all_categories': all_categories,
        'query': query,
        'selected_category': category_slug,
        'price_min': price_min,
        'price_max': price_max,
        'sort': sort,
        'tab': tab,
        'cart_item_count': cart_item_count,
    }
    return render(request, 'store/products.html', context)


def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(id=product.id)[:4]
    cart = get_cart(request)
    cart_item_count = cart.get_item_count()
    cart_form = CartAddForm()

    context = {
        'product': product,
        'related_products': related_products,
        'cart_form': cart_form,
        'cart_item_count': cart_item_count,
    }
    return render(request, 'store/product_detail.html', context)


def categories_view(request):
    categories = Category.objects.filter(parent__isnull=True)
    cart = get_cart(request)
    cart_item_count = cart.get_item_count()

    context = {
        'categories': categories,
        'cart_item_count': cart_item_count,
    }
    return render(request, 'store/categories.html', context)


def category_products_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(
        Q(category=category) | Q(category__parent=category),
        is_active=True
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

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    cart = get_cart(request)
    cart_item_count = cart.get_item_count()

    context = {
        'category': category,
        'products': page_obj,
        'sort': sort,
        'cart_item_count': cart_item_count,
    }
    return render(request, 'store/category_products.html', context)


def add_to_cart_view(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = get_cart(request)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product=product
        )
        if not created:
            cart_item.quantity += quantity
            if cart_item.quantity > product.stock:
                cart_item.quantity = product.stock
            cart_item.save()
        else:
            if quantity > product.stock:
                cart_item.quantity = product.stock
                cart_item.save()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'cart_count': cart.get_item_count(),
                'message': f'{product.name} added to cart!'
            })

        messages.success(request, f'{product.name} added to cart.')

    return redirect('products')


def remove_from_cart_view(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    product_name = cart_item.product.name
    cart = cart_item.cart
    cart_item.delete()
    messages.success(request, f'{product_name} removed from cart.')
    return redirect('cart')


def update_cart_view(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)

    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity < 1:
                quantity = 1
            if quantity > cart_item.product.stock:
                quantity = cart_item.product.stock
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated.')
        except (ValueError, TypeError):
            messages.error(request, 'Invalid quantity.')

    return redirect('cart')


def cart_view(request):
    cart = get_cart(request)
    cart_items = cart.items.select_related('product').all()
    cart_total = cart.get_total()
    cart_item_count = cart.get_item_count()
    delivery_fee = 200

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'delivery_fee': delivery_fee,
        'grand_total': cart_total + delivery_fee,
        'cart_item_count': cart_item_count,
    }
    return render(request, 'store/cart.html', context)


@login_required
def checkout_view(request):
    cart = get_cart(request)
    cart_items = cart.items.select_related('product').all()

    if not cart_items.exists():
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
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                )
                item.product.stock -= item.quantity
                if item.product.stock < 0:
                    item.product.stock = 0
                item.product.save()
            cart_items.delete()
            messages.success(request, 'Order placed successfully!')
            return redirect('order_confirmation', order_id=order.id)
    else:
        initial = {
            'full_name': f'{request.user.first_name} {request.user.last_name}'.strip(),
            'email': request.user.email,
            'city': 'Lahore',
        }
        form = CheckoutForm(initial=initial)

    context = {
        'form': form,
        'cart_items': cart_items,
        'cart_total': cart_total,
        'delivery_fee': delivery_fee,
        'grand_total': cart_total + delivery_fee,
        'cart_item_count': cart.get_item_count(),
    }
    return render(request, 'store/checkout.html', context)


@login_required
def order_confirmation_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    cart = get_cart(request)
    cart_item_count = cart.get_item_count()

    context = {
        'order': order,
        'cart_item_count': cart_item_count,
    }
    return render(request, 'store/order_confirmation.html', context)


@login_required
def order_history_view(request):
    orders = Order.objects.filter(user=request.user)
    cart = get_cart(request)
    cart_item_count = cart.get_item_count()

    context = {
        'orders': orders,
        'cart_item_count': cart_item_count,
    }
    return render(request, 'store/order_history.html', context)


def newsletter_view(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            newsletter, created = Newsletter.objects.get_or_create(email=email)
            if created:
                messages.success(request, 'Successfully subscribed to our newsletter!')
            else:
                messages.info(request, 'You are already subscribed.')
        else:
            messages.error(request, 'Please enter a valid email address.')

    return redirect(request.META.get('HTTP_REFERER', 'home'))


def search_view(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(is_active=True)

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(brand__icontains=query) |
            Q(category__name__icontains=query)
        )

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    cart = get_cart(request)
    cart_item_count = cart.get_item_count()

    context = {
        'products': page_obj,
        'query': query,
        'cart_item_count': cart_item_count,
    }
    return render(request, 'store/search_results.html', context)
