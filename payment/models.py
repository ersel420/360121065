from django.db import models
from account.models import UserBase
from website.models import Service

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(UserBase, on_delete = models.CASCADE)
    totalPaid = models.DecimalField(max_digits = 15, decimal_places = 2)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name_plural = 'Orders'
        ordering = ('-created',)

    def __str__(self):
        return str(self.created)

    @property
    def uID(self):
        return self.user.id

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete = models.CASCADE)
    service = models.ForeignKey(Service, on_delete = models.CASCADE)
    price = models.DecimalField(max_digits = 7, decimal_places = 2, default = 1)
    qty = models.PositiveIntegerField(default = 1)

    class Meta:
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return str(self.order.id)

    def total(self):
        return self.price * self.qty

    @property
    def sName(self):
        return self.service.name

    @property
    def sPrice(self):
        return self.service.price
    
    @property
    def sUrl(self):
        return self.service.get_absolute_url