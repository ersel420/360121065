from .cart import Cart
from .models import CartItem

def cart(request): #Cart Items
    return {'cart': Cart(request)}

# def cartQty(request): #Calculate Cart Qty
#     qty = 0
#     for item in CartItem.objects.filter(user = request.user):
#         qty += item.itemQty
#     return {'qty': qty}