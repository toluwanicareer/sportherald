from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    refresh_token=models.CharField(max_length=200)
    access_token=models.TextField(max_length=200)
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    posting_key=models.CharField(max_length=200, null=True)
    memo_key=models.CharField(max_length=200, null=True)
    active_key=models.CharField(max_length=200, null=True)


class Product(models.Model):
    title=models.CharField(max_length=200, null=True)
    manufacturer_url=models.URLField(null=True, max_length=800)
    image_url=models.URLField(null=True, max_length=200)
    search_term=models.CharField(null=True, max_length=200)
    price=models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    shipping = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    in_stock = models.BooleanField(default=True)
    sku = models.CharField(max_length=30, null=True, blank=True)
    details = models.CharField(max_length=800, null=True, blank=True)

    def __str__(self):
        return self.title




