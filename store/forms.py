from django import forms
from .models import Newsletter


class CartAddForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=99, initial=1, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'min': '1', 'max': '99'}
    ))


class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Full Name', 'id': 'full_name'}
    ))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email Address', 'id': 'email'}
    ))
    phone = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Phone Number (e.g. 03XXXXXXXXX)', 'id': 'phone'}
    ))
    address = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Street Address', 'rows': 3, 'id': 'address'}
    ))
    area = forms.CharField(max_length=100, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Area / Landmark', 'id': 'area'}
    ))
    city = forms.CharField(max_length=100, initial='Lahore', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'City', 'id': 'city', 'value': 'Lahore'}
    ))
    payment_method = forms.ChoiceField(
        choices=[
            ('cod', 'Cash on Delivery'),
            ('bank', 'Bank Transfer'),
            ('online', 'Online Payment'),
        ],
        widget=forms.RadioSelect(attrs={'class': 'payment-radio'})
    )


class NewsletterForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your email'}
    ))


class ContactForm(forms.Form):
    name = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Your Name'}
    ))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Your Email'}
    ))
    phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Phone Number'}
    ))
    subject = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Subject'}
    ))
    message = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 5}
    ))


class ProductSearchForm(forms.Form):
    query = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Search products...'}
    ))
