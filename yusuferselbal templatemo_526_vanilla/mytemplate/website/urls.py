# http://127.0.0.1:8000

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('index', views.home),
    path('services', views.services, name = 'services'),
    path('portfolio', views.portfolio, name = 'portfolio'),
    path('our-story', views.our_story, name = 'our_story'),
    path('contact-us', views.contact_us, name = 'contact_us'),
]
