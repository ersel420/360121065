from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from cart.cart import Cart
from cart.models import CartItem
import stripe
import iyzipay
import json
from django.http import HttpResponse
from .models import Order, OrderItem

options = {
    'api_key': 'sandbox-pgj9MQ5ZJVltOtVbCuPjwqy2OCcBmjku',
    'secret_key': 'sandbox-V79XOIdoYvRDPX52cDGY8Tmxp3Jk3uce',
    'base_url': 'sandbox-api.iyzipay.com',
}

tokenDict = list()

# Create your views here.
@login_required
def payView(request): #Pay Screen (Iyzico Template)
    currentUser = request.user
    if not currentUser.address:
        return redirect('account:edit')

    cartItems = []
    for item in CartItem.objects.filter(user = currentUser):
        cartItems.append({
            'id': str(item.sID),
            'name': str(item.sName),
            'category1': str(item.sCategory),
            'category2': str(item.sCategory),
            'itemType': 'VIRTUAL',
            'singlePrice': str(item.sPrice),
            'price': str(item.sPrice * item.itemQty),
        })
    
    userInfo = {
        'id': str(currentUser.id), #Other Format Example: BY789
        'name': str(currentUser.firstName),
        'surname': str(currentUser.lastName),
        'gsmNumber': str(currentUser.phoneNumber),
        'email': str(currentUser.email),
        'identityNumber': '74300864791', #Test ID
        'registrationAddress': str(currentUser.address),
        'ip': '192.168.1.1', #Test IP
        'city': 'Turkey', #Test City
        'country': 'Turkey', #Test Country
    }

    address = {
        'contactName': str(currentUser.firstName + ' ' + currentUser.lastName),
        'city': 'Turkey', #Test City
        'country': 'Turkey', #Test Country
        'address': str(currentUser.address),
    }

    request = {
        'locale': 'tr',
        'conversationId': '123456789',
        'price': str(totalPrice(request)),
        'paidPrice': str(totalPrice(request)),
        'currency': 'TRY',
        'basketId': 'B67832',
        'paymentGroup': 'PRODUCT',
        "callbackUrl": "http://127.0.0.1:8000/payment/orderplaced/",
        "enabledInstallments": ['1'],
        'buyer': userInfo,
        'shippingAddress': address,
        'billingAddress': address,
        'basketItems': cartItems,
        # 'debitCardAllowed': True
    }

    payForm = iyzipay.CheckoutFormInitialize().create(request, options)
    page = payForm
    header = {'Content-Type': 'application/json'}
    content = page.read().decode('utf-8')
    jsonContent = json.loads(content)
    tokenDict.append(jsonContent["token"])
    return HttpResponse(jsonContent["checkoutFormContent"])

@require_http_methods(['POST'])
@login_required
@csrf_exempt
def result(request): #Pay Request
    url = request.META.get('CSRF_TOKEN')

    request = {

        'locale': 'tr',
        'conversationId': '123456789',
        'token': tokenDict[0],
    }

    payResult = iyzipay.CheckoutForm().retrieve(request, options)
    result = payResult.read().decode('utf-8')
    jsonResult = json.loads(result, object_pairs_hook = list)

    if jsonResult[0][1] == 'success':
        return redirect('payment:success')
    elif jsonResult[0][1] == 'failure':
        return redirect('payment:fail')

    return HttpResponse(url)

def success(request): #Pay Success
    cart = Cart(request)
    cart.clear()

    order = Order.objects.create(user = request.user, totalPaid = totalPrice(request))
    for item in CartItem.objects.filter(user = request.user):
        OrderItem.objects.create(order = Order.objects.get(id = order.id), service = item.item, price = item.sPrice ,qty = item.itemQty)
    CartItem.objects.filter(user = request.user).delete()

    return render(request, 'payment/result.html', {'case': 'success'})

def fail(request): #Pay Fail
    return render(request, 'payment/result.html', {'case': 'fail'})

def totalPrice(request): #Get Total Price
    totalPrice = 0
    for item in CartItem.objects.filter(user = request.user): 
        totalPrice += item.sPrice * item.itemQty
    return totalPrice