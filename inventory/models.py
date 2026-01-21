from django.db import models
from accounts.models import User

# Create your models here.

class Product(models.Model):
    name=models.CharField(max_length=255 )
    sku=models.CharField(unique=True , max_length=100)
    cost_price=models.DecimalField(max_digits=10 , decimal_places=2)
    selling_price=models.DecimalField(max_digits=10 , decimal_places=2)
    stock_quantity=models.PositiveIntegerField(default=0)
    low_stock_threshold=models.PositiveIntegerField(default=5)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.name} ({self.sku})"


class Customer(models.Model):
    name=models.CharField(null=False, blank=False, max_length=100)
    phone_number=models.CharField(max_length=15 , unique=False , null=True , blank=True)
    address=models.TextField(null=True , blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name


class Supplier(models.Model):
    name=models.CharField(null=False, blank=False, max_length=100)
    phone_number=models.CharField(max_length=15 , unique=False , null=True , blank=True)
    address=models.TextField(null=True , blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name



  
    
    #   python manage.py makemigrations
    #   python manage.py migrate