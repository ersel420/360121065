from django.db import models
from decimal import Decimal
from django.conf import Settings
from website.models import Service

# Create your models here.
# class Order(models.Model):
    # user = models.ForeignKey(Settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'orderUser')
    # firstName = models.CharField(max_length = 50)
    # lastName = models.CharField(max_length = 50)
    # address = models.CharField(max_length = 500)
    # city = models.CharField(max_length = 50)
    # phone = models.CharField(max_length = 11)
    # postCode = models.CharField(max_length = 20)
    # created = models.DateTimeField(auto_now_add = True)
    # totalPaid = models.DecimalField(max_digits = 10, decimal_places = 2)
    # # orderKey = models.CharField(max_length = 200)
    # billingStatus = models.BooleanField(default = False)

    # class Meta:
        # ordering = ('-created',)

#     def __str__(self):
#         return str(self.created)

# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete = models.CASCADE, related_name = 'items')
#     service = models.ForeignKey(Service, on_delete = models.CASCADE, related_name = 'orderItems')
#     price = models.DecimalField(max_digits = 10, decimal_places = 2)
#     quantity = models.PositiveIntegerField(default = 1)

#     def __str__(self):
#         return str(self.id)