from django.contrib import admin
from django import forms
from .models import Category, Product, Cart, CartItem, Order, OrderItem, Newsletter


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if hasattr(image, 'size') and image.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Image file size must be under 5MB.')
        return image


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent', 'sort_order', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('parent',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('name', 'category', 'brand', 'weight', 'price', 'old_price', 'stock', 'is_active', 'is_featured', 'is_bestseller', 'rating')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('category', 'is_active', 'is_featured', 'is_bestseller', 'brand')
    search_fields = ('name', 'brand', 'description')
    fields = ('name', 'slug', 'category', 'brand', 'weight', 'description', 'price', 'old_price', 'discount_percent', 'image', 'image_url', 'stock', 'rating', 'is_active', 'is_featured', 'is_bestseller', 'is_new_arrival')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_key', 'created_at')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'added_at')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'total_amount', 'status', 'payment_method', 'city', 'created_at')
    list_filter = ('status', 'payment_method', 'city')
    search_fields = ('full_name', 'email', 'phone')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')
