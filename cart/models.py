from django.db import models
from account.models import UserBase
from website.models import Service

# Create your models here.
class CartItem(models.Model):
    user = models.ForeignKey(UserBase, on_delete = models.CASCADE)
    item =  models.ForeignKey(Service, on_delete = models.CASCADE)
    itemQty = models.IntegerField()

    class Meta:
        verbose_name_plural = "Cart Items"

    def __str__(self):
        return str(self.user)

    @property
    def sCategory(self):
        return self.item.cName

    @property
    def sDescription(self):
        return self.item.description

    @property
    def sImageUrl(self):
        return self.item.image.url

    @property
    def sName(self):
        return self.item.name

    @property
    def sID(self):
        return self.item.id

    @property
    def sPrice(self):
        return self.item.price
    
    @property
    def sUrl(self):
        return self.item.get_absolute_url