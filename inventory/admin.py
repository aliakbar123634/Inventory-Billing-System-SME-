from django.contrib import admin
from .models import Product , Supplier , Customer

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "sku", "stock_quantity","low_stock_threshold" , "selling_price", "is_active", "created_at")
    search_fields = ("name", "sku")
    list_filter = ("is_active",)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone_number", "address","created_at")

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone_number", "address","created_at")