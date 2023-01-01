from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .cart import Cart
from .models import CartItem
from website.models import Service

# Create your views here.
@login_required
def cartSummary(request): #Cart Page
    cart = Cart(request)
    return render(request, 'cart/summary.html', {
        'cart': CartItem.objects.filter(user = request.user),
        'total': cartTotal(request),
    })


def cartAdd(request): #Add Item to Cart
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        serviceID = int(request.POST.get('serviceid'))
        serviceQty = int(request.POST.get('serviceqty'))
        service = get_object_or_404(Service, id = serviceID)
        cart.add(service = service, qty = serviceQty)

        if not CartItem.objects.filter(user = request.user, item = Service.objects.get(id = serviceID)):
            CartItem.objects.create(user = request.user, item = Service.objects.get(id = serviceID), itemQty = serviceQty)
        else:
            CartItem.objects.filter(user = request.user, item = Service.objects.get(id = serviceID)).update(itemQty = serviceQty)
        
        cartQty = cart.__len__()
        cartTotal = cart.cartTotal()
        response = JsonResponse({
            'qty': cartQty,
            'ttl': cartTotal,
        })
        return response

def cartDelete(request): #Delete Item from Cart
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        serviceID = int(request.POST.get('serviceid'))
        cart.delete(service = serviceID)

        CartItem.objects.filter(user = request.user, item = Service.objects.get(id = serviceID)).delete()

        cartQty = cart.__len__()
        cartTotal = cart.cartTotal()
        response = JsonResponse({
            'qty': cartQty,
            'subtotal': cartTotal,
        })
        return response

def cartUpdate(request): #Update Item from Cart
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        serviceID = int(request.POST.get('serviceid'))
        serviceQty = int(request.POST.get('serviceqty'))
        cart.update(service = serviceID, qty = serviceQty)

        CartItem.objects.filter(user = request.user, item = Service.objects.get(id = serviceID)).update(itemQty = serviceQty)

        cartQty = cart.__len__()
        cartTotal = cart.cartTotal()
        response = JsonResponse({
            'qty': cartQty,
            'subtotal': cartTotal,
        })
        return response

def cartTotal(request): #Calculate Cart Total
    total = 0
    for item in CartItem.objects.filter(user = request.user):
        total += item.sPrice * item.itemQty
    return total