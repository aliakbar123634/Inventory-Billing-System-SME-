from rest_framework import serializers
from django.db import transaction
from decimal import Decimal
from . models import *
from django.db.models import Sum





class PurchaseItemSerializer(serializers.ModelSerializer):
    line_total=serializers.DecimalField(max_digits=15 , decimal_places=2 , read_only=True)
    class Meta:
        model=PurchaseItem
        fields=['id' , 'product' , 'qty' , 'unit_cost' , 'line_total' ]
        read_only_fields=('id' , 'line_total')

    def validate_qty(self , value):
        if value <= 0 :
            raise serializers.ValidationError("quantity must be greater than zero..")
        return value
    def validate_unit_cost(self  , value):
        if value <0:
            raise serializers.ValidationError("unit cost  must be greater than zero..")
        return value            
        
class PurchaseInvoiceSerialier(serializers.ModelSerializer):
    items=PurchaseItemSerializer(many=True) 
    total_amount=serializers.DecimalField(max_digits=15 , decimal_places=2 , read_only=True) 
    created_by=serializers.PrimaryKeyRelatedField(read_only=True)   
    class Meta:
        model=PurchaseInvoice
        fields=['id' , 'invoice_no' , 'supplier' , 'note' , 'items' ,'created_at' , 'total_amount' , 'created_by']
        read_only_fields=('id' , 'created_at' , 'total_amount' , 'created_by')

    def validate(self , attrs):
        items=attrs.get("items" , [])
        if not items:
            raise serializers.ValidationError("At least one purchase iteem is required...")
        return attrs
    
    @transaction.atomic
    def create(self , validated_data):
        items=validated_data.pop('items')
        request=self.context.get('request')
        user=request.user if request else None

        purchase_invoice=PurchaseInvoice.objects.create(
            **validated_data,
            created_by=user,
            total_amount=Decimal("0.00")
        )
        total_amount=Decimal("0.00")
        for item in items:
            product=item['product']
            qty=item['qty']
            unit_cost=item['unit_cost']

            line_total=qty * unit_cost
            total_amount += line_total
            PurchaseItem.objects.create(
                invoice=purchase_invoice,
                product=product,
                qty=qty,
                unit_cost=unit_cost,
                line_total=line_total  
            )

            # update product
            product.stock_quantity += qty
            product.save()     
            
        purchase_invoice.total_amount=total_amount
        purchase_invoice.save()
        return purchase_invoice          


class SaleItemSerializer(serializers.ModelSerializer):
    line_total=serializers.DecimalField(max_digits=15 , decimal_places=2 , read_only=True)
    class Meta:
        model=SaleItem
        fields=['id' , 'product' , 'qty' , 'unit_price_salesItem' , 'line_total']
        read_only_fields=['id', 'line_total']
    def validate_qty(self , value):
        if value <= 0 :
            raise serializers.ValidationError("quantity must be greater than zero...") 
        return value

    def validate_unit_price_salesItem(self , value):
        if value <=0 :     
            raise serializers.ValidationError("unit price must be greater than zero...") 
        return value

class SaleInvoiceSerializer(serializers.ModelSerializer):
    purchaseitems=SaleItemSerializer(many=True)
    total_amount=serializers.DecimalField(max_digits=15 , decimal_places=2 , read_only=True)  
    created_by=serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:  
        model = SaleInvoice 
        fields=['id' , 'invoice_no' , 'customer' , 'note' , 'payment_status' ,'purchaseitems' , 'total_amount' , 'created_by' , 'created_at']   
        read_only_fields=['total_amount' , 'created_by' , 'created_at']

    def validate(self , attrs):
        items=attrs.get('purchaseitems' , [])
        if not items:
            raise serializers.ValidationError("atleast one sale item is required...")   
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        items_data=validated_data.pop('purchaseitems')
        request=self.context.get('request')
        if request:
            user=request.user
        else:
            user=None
        
        invoice=SaleInvoice.objects.create(
            **validated_data, 
            created_by=user,
            total_amount=Decimal("0.00")
        )
        total_amount = Decimal("0.00")

        for item in items_data:
            product=item.get('product')
            qty=item.get('qty')
            unit_price_salesItem=item.get('unit_price_salesItem')
            
            line_total = qty * unit_price_salesItem
            total_amount=total_amount+line_total
            if product.stock_quantity < qty:
                raise serializers.ValidationError(
                    {"stock": f"Not enough stock for {product.name}. Available: {product.stock_quantity}"}
                )            

            SaleItem.objects.create(
                invoice=invoice,
                product=product,
                qty=qty,
                unit_price_salesItem=unit_price_salesItem,
                line_total=line_total
            )

            product.stock_quantity-=qty
            product.save()
        invoice.total_amount= total_amount   
        invoice.save()
        return invoice 


class SalePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalePayment
        fields = ["id", "invoice", "amount", "method", "note", "paid_by", "paid_at"]
        read_only_fields = ["id", "paid_by", "paid_at"]

    def validate(self, attrs):
        invoice = attrs.get("invoice")
        if not invoice:
            raise serializers.ValidationError("Invoice is required.")

        amount = attrs.get("amount")
        if amount is None or amount <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")

        total_paid = invoice.payments.aggregate(total=Sum("amount"))["total"] or 0
        due = invoice.total_amount - total_paid

        if amount > due:
            raise serializers.ValidationError("Payment cannot exceed due amount.")

        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user if request else None
        validated_data["paid_by"] = user

        invoice = validated_data["invoice"]

        payment = SalePayment.objects.create(**validated_data)

        # Recalculate total paid after this payment
        total_paid = invoice.payments.aggregate(total=Sum("amount"))["total"] or 0

        # Update invoice payment status
        if total_paid == 0:
            invoice.payment_status = "UNPAID"
        elif total_paid < invoice.total_amount:
            invoice.payment_status = "PARTIAL"
        else:
            invoice.payment_status = "PAID"

        invoice.save()
        return payment
    
    

class SupplierPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierPayment
        fields = ["id", "invoice", "amount", "method", "note", "paid_by", "paid_at"]
        read_only_fields = ["id", "paid_by", "paid_at"]

    def validate(self, attrs):
        invoice = attrs.get("invoice")
        if not invoice:
            raise serializers.ValidationError("Invoice is required.")

        amount = attrs.get("amount")
        if amount is None or amount <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")

        # Reverse FK: invoice.payments
        total_paid = invoice.payments.aggregate(total=Sum("amount"))["total"] or 0

        due = invoice.total_amount - total_paid
        if due < 0:
            due = 0  # Extra safety

        if amount > due:
            raise serializers.ValidationError(
                f"Payment cannot exceed due amount. Due = {due}"
            )

        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user if request else None

        validated_data["paid_by"] = user
        invoice = validated_data["invoice"]

        # 1) Create Payment Entry
        payment = SupplierPayment.objects.create(**validated_data)

        # 2) Recalculate Total Paid
        total_paid = invoice.payments.aggregate(total=Sum("amount"))["total"] or 0

        # 3) Update Status
        if total_paid == 0:
            invoice.payment_status = "UNPAID"
        elif total_paid < invoice.total_amount:
            invoice.payment_status = "PARTIAL"
        else:
            invoice.payment_status = "PAID"

        invoice.save(update_fields=["payment_status"])

        return payment
