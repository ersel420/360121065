from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('', views.payView, name='pay'), #Payment Page (Iyzico Template)
    path('orderplaced/', views.result, name="order-placed"), #Pay Request
    path('ordersuccess/', views.success, name = 'success'), #Pay Success
    path('orderfail/', views.fail, name = 'fail') #Pay Fail
]

