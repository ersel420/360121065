from .cart import Cart

def cart(request): #Cart Items
    return {'cart': Cart(request)}