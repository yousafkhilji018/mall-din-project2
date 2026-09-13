from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('stores/', views.stores_view, name='stores'),
    path('dining/', views.dining_view, name='dining'),
    path('entertainment/', views.entertainment_view, name='entertainment'),
]
