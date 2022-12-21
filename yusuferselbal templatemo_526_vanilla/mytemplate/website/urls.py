# http://127.0.0.1:8000

from django.urls import path
from . import views

# app_name = 'website'

urlpatterns = [
    path('', views.home, name = 'home'),
    path('index', views.home),
    path('services', views.services, name = 'services'),
    path('portfolio', views.portfolio, name = 'portfolio'),
    path('our-story', views.our_story, name = 'our_story'),
    path('contact-us', views.contact_us, name = 'contact_us'),
    path('login', views.login, name = 'login'),
    path('register', views.register, name = 'register'),
    path('profile', views.profile, name = 'profile'),
    path('cart', views.cart, name = 'cart'),
    path('search/<slug:category_slug>/', views.categoryFilter, name="categoryFilter"),
    # path('service/<slug:slug>/', views.serviceDetail, name="serviceDetail")
]
