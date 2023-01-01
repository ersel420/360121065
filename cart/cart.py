from django.conf import settings
from decimal import Decimal
from website.models import Service

class Cart(): #Base Cart Class
    def __init__(self, request): #Initial Function
        self.session = request.session
        cart = self.session.get('skey')
        if 'skey' not in request.session:
            cart = self.session['skey'] = {}
        self.cart = cart

    def add(self, service, qty): #Add Data to Session
        serviceID = str(service.id)
        if serviceID in self.cart:
            self.cart[serviceID]['qty'] = qty
        else:
            self.cart[serviceID] = {
                'price': str(service.price),
                'qty': qty,
            }

        self.save()

    def __iter__(self): #Iterate Data to Cart
        serviceIDs = self.cart.keys()
        services = Service.objects.filter(id__in = serviceIDs)
        cart = self.cart.copy()

        for service in services:
            cart[str(service.id)]['service'] = service

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['totalPrice'] = item['price'] * item['qty']
            yield item

    def __len__(self): #Counting Quantity
        return sum(item['qty'] for item in self.cart.values())

    def cartTotal(self): #Total Cart Price
        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())

    def delete(self, service): #Delete Data from Session
        serviceID = str(service)
        if serviceID in self.cart:
            del self.cart[serviceID]

        self.save()

    def update(self, service, qty): #Update Data from Session
        serviceID = str(service)
        if serviceID in self.cart:
            self.cart[serviceID]['qty'] = qty

        self.save()

    def clear(self): #Delete Everything in Cart
        del self.session['skey']
        self.save()

    def save(self): #Session Modified
        self.session.modified = True