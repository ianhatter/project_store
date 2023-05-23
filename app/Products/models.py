from django.db import models

# Create your models here.
class Products(models.Model):
    Product_name = models.CharField(max_length=70, blank=False, default='')
    Product_SKU = models.CharField(max_length=200, blank=False, default='')
    description = models.CharField(max_length=200, blank=False, default='')
    published = models.BooleanField(default=False)