from django.db import models
from django.db.models.functions import Now
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

# class User(models.Model):
#     firstName = models.CharField(max_length = 30)
#     lastName = models.CharField(max_length = 30)
#     userName = models.CharField(max_length = 30)
#     telephone = models.CharField(max_length = 11)
#     email = models.CharField(max_length = 50)
#     password = models.CharField(max_length = 50)
#     superUser = models.BooleanField(default = False)

class Category(models.Model):
    name = models.CharField(max_length = 100, db_index = True)
    slug = models.SlugField(max_length = 105, unique = True)

    class Meta:
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('website:categoryFilter', args = [self.slug])
        # return reverse("categoryFilter", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name
    
class Service(models.Model):
    category =  models.ForeignKey(Category, related_name = 'service', on_delete=models.CASCADE)
    name = models.CharField(max_length = 100)
    description = models.TextField(blank = True)
    image = models.ImageField(upload_to = 'static/website/img/')
    bigImage = models.ImageField(upload_to = 'static/website/img/')
    slug = models.SlugField(max_length = 105, unique = True)
    price = models.DecimalField(max_digits = 7, decimal_places = 2)
    is_active = models.BooleanField(default = True)

    class Meta:
        verbose_name_plural = 'Services'

    def get_absolute_url(self):
        return reverse('website:serviceDetail', args = [self.slug])

    def __str__(self):
        return self.name

    # name = models.CharField(max_length = 100)
    # image = models.CharField(max_length = 100)
    # bigImage = models.CharField(max_length = 100 )
    # price = models.DecimalField(max_digits = 10, decimal_places = 2)
    # categoryID = models.ForeignKey(Category, default=1, on_delete=models.CASCADE)

# class Order(models.Model):
#     serviceID = models.ForeignKey(Service, on_delete=models.CASCADE)
#     # userID = models.ForeignKey(User, on_delete=models.CASCADE)
#     orderDate = models.DateTimeField(default = Now)
#     orderDetails = models.CharField(max_length = 1000)

# class Department(models.Model):
#     name = models.CharField(max_length = 30)

# class Employee(models.Model):
#     firstName = models.CharField(max_length = 30)
#     lastName = models.CharField(max_length = 30)
#     deptID = models.ForeignKey(Department, on_delete = models.CASCADE)
#     salary = models.DecimalField(max_digits = 10, decimal_places = 2)

# class WorkingOn(models.Model):
#     employeeID = models.ForeignKey(Employee, on_delete = models.CASCADE)
#     orderID = models.ForeignKey(Order, on_delete = models.CASCADE)