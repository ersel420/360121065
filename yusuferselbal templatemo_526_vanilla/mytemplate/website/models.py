from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 100, db_index = True)
    slug = models.SlugField(max_length = 105, unique = True)

    class Meta:
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('website:categoryFilter', args = [self.slug])

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

    @property
    def cName(self):
        return self.category.name