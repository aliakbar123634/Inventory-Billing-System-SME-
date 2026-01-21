
from decimal import Decimal
from accounts import models
from inventory.models import Product , Supplier , Customer 
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id' , 'name' , 'sku' , 'cost_price' , 'selling_price' , 'low_stock_threshold', "is_active", 'stock_quantity' , 'created_at']
        read_only_fields=('id','created_at')

    def validate(self , attrs):
        selling_price=attrs.get('selling_price' , self.instance.selling_price if self.instance else None ) 
        cost_price=attrs.get('cost_price' , self.instance.cost_price if self.instance else None ) 
        stock_quantity=attrs.get('stock_quantity' , self.instance.stock_quantity if self.instance else None ) 
        low_stock_threshold=attrs.get('low_stock_threshold' , self.instance.low_stock_threshold if self.instance else None ) 
        if selling_price is not None and cost_price is not None:
            if selling_price < cost_price:
                raise serializers.ValidationError("selling price cannot less than cost price...")
        if stock_quantity is not None and stock_quantity < 0:
            raise serializers.ValidationError("stock cannot be negative...")
        if low_stock_threshold is not None and low_stock_threshold < 5:
            raise serializers.ValidationError("low stock threshold cannot be negative and less than 5...")
        return attrs
    def validate_name(self , value):
        if not value or not value.strip():
            raise serializers.ValidationError("product name cannot be empty or whitespaces..")
        return value
        

            
class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model=Supplier
        fields=['id' , 'name' , 'phone_number' , 'address' , 'created_at']
        read_only_fields=('id','created_at')

    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Supplier name cannot be empty or whitespaces..")
        return value

    def validate_phone_number(self , value):
        if value and not value.isdigit():
            raise serializers.ValidationError("phone number must contain digits only ...")
        return value
        
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields=['id' , 'name' , 'phone_number' , 'address' , 'created_at']
        read_only_fields=('id','created_at')

    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Customer name cannot be empty or whitespaces..")
        return value

    def validate_phone_number(self , value):
        if value and not value.isdigit():
            raise serializers.ValidationError("phone number must contain digits only ...")
        return value        






        

        

            
