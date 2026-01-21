from django.shortcuts import render
from .models import *
from .serializer import *
from rest_framework import viewsets ,filters
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
# Create your views here.



class PurchaseInvoiceViewSet(viewsets.ModelViewSet):
    queryset=(
        PurchaseInvoice.objects.all()
        .select_related('supplier' , 'created_by')
        .prefetch_related('items' , 'items__product')
    )
    serializer_class=PurchaseInvoiceSerialier
    permission_classes=[IsAuthenticated]
    filter_backends=[filters.SearchFilter , filters.OrderingFilter]
    search_fields=['invoice_no' , 'supplier__name']
    ordering_fields=['created_at']
    ordering = ["-created_at"]


class SaleInvoiceViewSet(viewsets.ModelViewSet):
    queryset=(
        SaleInvoice.objects.all()
        .select_related('customer' , 'created_by')
        .prefetch_related('purchaseitems' , 'purchaseitems__product')
         )
    serializer_class=SaleInvoiceSerializer
    permission_classes=[IsAuthenticated]
    http_method_names=['get' , 'post']
    filter_backends=[filters.SearchFilter , filters.OrderingFilter]
    search_fields=['invoice_no' , 'customer__name']
    ordering_fields=['created_at']
    ordering = ["-created_at"]    

class SalePaymentViewset(viewsets.ModelViewSet):
    queryset=(
        SalePayment.objects.all()
        .select_related("invoice", "paid_by")
    )   
    serializer_class=SalePaymentSerializer
    permission_classes=[IsAuthenticated]
    http_method_names=['get' , 'post']



class SupplierPaymenViewSet(viewsets.ModelViewSet):
    queryset=(
        SupplierPayment.objects.all()
        .select_related(
            "invoice", "paid_by"
        )
    )   
    serializer_class=SupplierPaymentSerializer
    permission_classes=[IsAuthenticated]
    http_method_names = ["get", "post"]
        