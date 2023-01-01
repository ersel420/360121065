from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    #Main Pages
    path('', views.home, name = 'home'), #Homepage
    path('index/', views.home), #Homepage (İndex)
    path('info/', views.info, name = 'info'), #Info Page
    path('our-story/', views.our_story, name = 'our_story'), #Our Story Page
    path('contact-us/', views.contact_us, name = 'contact_us'), #Contact Us Page

    #Service Pages
    path('services/', views.services, name = 'services'), #Service Page
    path('services/<slug:slug>/', views.serviceDetail, name="serviceDetail"), #Service Details Page
    path('search/<slug:category_slug>/', views.categoryFilter, name="categoryFilter"), #Category Filter Page
]
