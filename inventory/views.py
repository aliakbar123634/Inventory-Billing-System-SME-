from django.shortcuts import render
from rest_framework import viewsets ,filters
from .models import Product, Supplier , Customer 
from accounts.models import User
from .serilizer import ProductSerializer , SupplierSerializer , CustomerSerializer 
from .permissions import  IsOwnerOrReadOnly , IsOwnerforDeleteElseAuthenticated
from django.db.models import F




# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter , filters.OrderingFilter]
    search_fields=['name' , 'sku']
    ordering_fields=['cost_price' , 'selling_price' , 'stock_quantity' , 'created_at']
    ordering = ["-created_at"] 

    def get_queryset(self):
        qs=Product.objects.all()
        request=self.request
        print(request)
        params = request.query_params
        print(params)

        is_active = params.get('is_active')
        if is_active:
            is_active = is_active.lower()
            if is_active in ['true', 'false']:
                qs = qs.filter(is_active=(is_active == 'true'))

        low_stock = params.get('low_stock')
        if low_stock:
            low_stock = low_stock.lower()
            if low_stock == 'true':
                qs = qs.filter(stock_quantity__lte=F("low_stock_threshold"))


        return qs    


class SupplierViewSet(viewsets.ModelViewSet):
    queryset=Supplier.objects.all()
    serializer_class=SupplierSerializer
    permission_classes=[IsOwnerforDeleteElseAuthenticated]
    filter_backends= [filters.SearchFilter , filters.OrderingFilter]
    search_fields=['name' , 'phone_number']
    ordering_fields=[ 'created_at']
    ordering = ["-created_at"]


class CustomerViewSet(viewsets.ModelViewSet): 
    queryset=Customer.objects.all() 
    serializer_class=CustomerSerializer 
    permission_classes=[IsOwnerforDeleteElseAuthenticated] 
    filter_backends= [filters.SearchFilter , filters.OrderingFilter]
    search_fields=['name' , 'phone_number']
    ordering_fields=[ 'created_at']
    ordering = ["-created_at"]