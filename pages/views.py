from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20, required=False)
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)


def about_view(request):
    stats = {
        'products': '10,000+',
        'departments': '4+',
        'customers': '50K+',
        'years': '5+',
    }
    context = {'stats': stats}
    return render(request, 'pages/about.html', context)


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Thank you for your message! We will get back to you shortly.')
            return redirect('contact')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()
    context = {'form': form}
    return render(request, 'pages/contact.html', context)


def stores_view(request):
    stores = [{
        'name': 'MALL DIN Cash & Carry',
        'floor': 'Main Store',
        'category': 'Grocery',
        'hours': '8:00 AM - 11:00 PM',
        'phone': '+92 321 1234567',
        'description': 'Your one-stop shop for groceries, household essentials, personal care products and more.',
    }]
    context = {'stores': stores}
    return render(request, 'pages/stores.html', context)


def dining_view(request):
    restaurants = [
        {'name': 'Food Court', 'cuisine': 'Multi-Cuisine', 'floor': 'Ground Floor', 'hours': '10:00 AM - 11:00 PM', 'rating': 4.5, 'description': 'Multiple food stalls offering Pakistani, Chinese, and fast food options.', 'price_range': 'PKR 200 - 800'},
        {'name': 'Chai Corner', 'cuisine': 'Beverages', 'floor': 'Ground Floor', 'hours': '8:00 AM - 11:00 PM', 'rating': 4.7, 'description': 'Premium teas, coffees, and freshly baked items in a cozy setting.', 'price_range': 'PKR 50 - 300'},
        {'name': 'Family Restaurant', 'cuisine': 'Pakistani', 'floor': 'First Floor', 'hours': '12:00 PM - 12:00 AM', 'rating': 4.6, 'description': 'Authentic Pakistani cuisine with traditional BBQ and biryani.', 'price_range': 'PKR 300 - 1,500'},
    ]
    cuisine = request.GET.get('cuisine', 'All')
    if cuisine != 'All':
        restaurants = [r for r in restaurants if r['cuisine'] == cuisine]
    context = {'restaurants': restaurants, 'current_cuisine': cuisine, 'cuisines': ['All', 'Pakistani', 'Multi-Cuisine', 'Beverages']}
    return render(request, 'pages/dining.html', context)


def entertainment_view(request):
    venues = [
        {'name': 'Kids Play Area', 'type': 'Kids', 'floor': 'First Floor', 'hours': '10:00 AM - 9:00 PM', 'description': 'Safe and fun indoor playground for children of all ages.', 'price': 'PKR 200 - 500'},
        {'name': 'Events Hall', 'type': 'Events', 'floor': 'Second Floor', 'hours': 'By Booking', 'description': 'Premium event space for celebrations, corporate events, and special occasions.', 'price': 'Starting PKR 50,000'},
        {'name': 'Activity Zone', 'type': 'Activities', 'floor': 'First Floor', 'hours': '10:00 AM - 10:00 PM', 'description': 'Fun activities and entertainment for the whole family.', 'price': 'PKR 100 - 500'},
    ]
    venue_type = request.GET.get('type', 'All')
    if venue_type != 'All':
        venues = [v for v in venues if v['type'] == venue_type]
    context = {'venues': venues, 'current_type': venue_type, 'types': ['All', 'Kids', 'Events', 'Activities']}
    return render(request, 'pages/entertainment.html', context)
