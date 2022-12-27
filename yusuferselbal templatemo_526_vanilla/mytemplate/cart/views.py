from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .cart import Cart
from website.models import Service

# Create your views here.
def cartSummary(request): #Cart Page
    cart = Cart(request)
    return render(request, 'cart/summary.html', {'cart': cart})

def cartAdd(request): #Add Item to Cart
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        serviceID = int(request.POST.get('serviceid'))
        serviceQty = int(request.POST.get('serviceqty'))
        service = get_object_or_404(Service, id = serviceID)
        cart.add(service = service, qty = serviceQty)
        
        cartTotal = cart.cartTotal()
        cartQty = cart.__len__()
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
        cartQty = cart.__len__()
        cartTotal = cart.cartTotal()
        response = JsonResponse({
            'qty': cartQty,
            'subtotal': cartTotal,
        })
        return response