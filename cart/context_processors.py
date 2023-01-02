from .cart import Cart
from .models import CartItem

def cart(request): #Cart Items
    return {'cart': Cart(request)}
