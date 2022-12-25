from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cartSummary, name = 'cartSummary'), #User Cart Page
    path('add/', views.cartAdd, name = 'cartAdd'), #Add Item to Cart
    path('delete/', views.cartDelete, name = 'cartDelete'), #Delete Item from Cart
    path('update/', views.cartUpdate, name = 'cartUpdate'), #Update Item from Cart

]
