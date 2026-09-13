from django.urls import path
from . import views

urlpatterns = [
    path('', views.products_view, name='products'),
    path('product/<slug:slug>/', views.product_detail_view, name='product_detail'),
    path('categories/', views.categories_view, name='categories'),
    path('category/<slug:slug>/', views.category_products_view, name='category_products'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart_view, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart_view, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_view, name='update_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order/<int:order_id>/', views.order_confirmation_view, name='order_confirmation'),
    path('orders/', views.order_history_view, name='order_history'),
    path('newsletter/', views.newsletter_view, name='newsletter'),
    path('search/', views.search_view, name='search'),
]
