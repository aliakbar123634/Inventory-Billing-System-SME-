from django.contrib import admin
from . models import *


@admin.register(PurchaseInvoice)
class PurchaseInvoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "invoice_no", "supplier", "note","total_amount" , "created_at" , "created_by")
    search_fields = ("invoice_no", "supplier")
    list_filter = ("id",)


@admin.register(PurchaseItem)
class PurchaseItemAdmin(admin.ModelAdmin):
    list_display = ("id", "invoice", "product", "qty","unit_cost" , "line_total" )
    search_fields = ("invoice", "product")
    list_filter = ("id",)


@admin.register(SaleInvoice)
class SaleInvoiceInvoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "invoice_no", "customer", "note","total_amount" ,"payment_status", "created_at" , "created_by")
    search_fields = ("invoice_no", "customer")
    list_filter = ("id",)

@admin.register(SaleItem)
class SaleItemItemAdmin(admin.ModelAdmin):
    list_display = ("id", "invoice", "product", "qty","unit_price_salesItem" , "line_total" )
    search_fields = ("invoice", "product")
    list_filter = ("id",)    