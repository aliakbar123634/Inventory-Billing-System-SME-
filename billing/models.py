from django.db import models
from inventory.models import Supplier , Product , Customer
from accounts.models import User
from billing.models import *
from django.core.validators import MinValueValidator


# Create your models here.

class PurchaseInvoice(models.Model):
    CHOICE_STATUS = (
    ("PAID", "Paid"),
    ("UNPAID", "Unpaid"),
    ("PARTIAL", "Partial"),
    )
    invoice_no=models.CharField(max_length=100 ,null=True , blank=True , unique=True )
    supplier=models.ForeignKey(Supplier , on_delete=models.CASCADE)
    note=models.TextField(null=True , blank=True)
    total_amount=models.DecimalField(max_digits=15 , decimal_places=2 , default=0)
    payment_status=models.CharField(max_length=10 , choices=CHOICE_STATUS , default="UNPAID")
    created_by=models.ForeignKey(User , on_delete=models.SET_NULL , null=True , blank=True )
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.invoice_no or 'N/A'} - {self.supplier.name}"
    
class PurchaseItem(models.Model):
    invoice=models.ForeignKey(PurchaseInvoice , on_delete=models.CASCADE , related_name="items")
    product=models.ForeignKey(Product , on_delete=models.CASCADE)
    qty=models.PositiveIntegerField()
    unit_cost=models.DecimalField(max_digits=10 , decimal_places=2)
    line_total=models.DecimalField(max_digits=15 , decimal_places=2 , default=0)

    def __str__(self):
        return f"{self.invoice.invoice_no or 'N/A'} - {self.product.name}" 
    

class SaleInvoice(models.Model):
    CHOICE_STATUS = (
    ("PAID", "Paid"),
    ("UNPAID", "Unpaid"),
    ("PARTIAL", "Partial"),
    )
    invoice_no=models.CharField(max_length=100 ,null=True , blank=True , unique=True )
    customer=models.ForeignKey(Customer , on_delete=models.CASCADE)
    note=models.TextField(null=True , blank=True)
    total_amount=models.DecimalField(max_digits=15 , decimal_places=2 , default=0)
    payment_status=models.CharField(max_length=10 , choices=CHOICE_STATUS , default="UNPAID")
    created_by=models.ForeignKey(User , on_delete=models.SET_NULL , null=True , blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.invoice_no or 'N/A'} - {self.customer.name}"     


class SaleItem(models.Model):
    invoice=models.ForeignKey(SaleInvoice , on_delete=models.CASCADE , related_name="purchaseitems")  
    product=models.ForeignKey(Product , on_delete=models.CASCADE)  
    qty=models.PositiveIntegerField()
    unit_price_salesItem=models.DecimalField(max_digits=10 , decimal_places=2)
    line_total=models.DecimalField(max_digits=15 , decimal_places=2 , default=0)

    def __str__(self):
        return f"{self.invoice.invoice_no or 'N/A'} - {self.product.name}"



class SalePayment(models.Model):
    PAYMENT_METHODS = (
    ("CASH", "cash"),
    ("BANK", "bank"),
    ("EASYPAISA", "easypaisa"),
    ("JAZZCASH", "jazzcash")
    )    
    invoice=models.ForeignKey(SaleInvoice , on_delete=models.CASCADE , related_name="payments")  
    amount=models.DecimalField(max_digits=15, decimal_places=2 , validators=[MinValueValidator(0.01)])   
    method=models.CharField(max_length=10 , choices=PAYMENT_METHODS , default="CASH")  
    note=models.TextField(null=True , blank=True) 
    paid_by=models.ForeignKey(User  , on_delete=models.SET_NULL , null=True , blank=True)
    paid_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.invoice.invoice_no or self.invoice.id} - {self.amount} ({self.method})"
    

class SupplierPayment(models.Model):
    PAYMENT_METHODS = (
    ("CASH", "cash"),
    ("BANK", "bank"),
    ("EASYPAISA", "easypaisa"),
    ("JAZZCASH", "jazzcash")
    )    
    invoice=models.ForeignKey(PurchaseInvoice , on_delete=models.CASCADE , related_name="payments")  
    amount=models.DecimalField(max_digits=15, decimal_places=2 , validators=[MinValueValidator(0.01)])   
    method=models.CharField(max_length=10 , choices=PAYMENT_METHODS , default="CASH")  
    note=models.TextField(null=True , blank=True) 
    paid_by=models.ForeignKey(User  , on_delete=models.SET_NULL , null=True , blank=True)
    paid_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.invoice.invoice_no or self.invoice.id} - {self.amount} ({self.method})"    
    
    #   python manage.py makemigrations
    #   python manage.py migrate