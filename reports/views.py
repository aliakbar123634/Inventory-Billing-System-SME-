from django.shortcuts import render , get_object_or_404
from inventory.models import Product
from inventory.serilizer import ProductSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime
# from .serializer import SupplierPaymentSerializer
from rest_framework.permissions import IsAuthenticated 
from billing.models import SaleInvoice  , SaleItem , Customer , SupplierPayment , Supplier , PurchaseInvoice
from billing.serializer import SaleInvoiceSerializer
from rest_framework import status
from rest_framework import viewsets
from django.db.models import F , Sum , Count , ExpressionWrapper , DecimalField 


# Create your views here.

class LowStockProductsView(APIView):

    permission_classes = [IsAuthenticated]
    def get(self , request):
        products=Product.objects.filter(stock_quantity__lte=F("low_stock_threshold"))
        serializer=ProductSerializer(products , many=True)
        return Response(serializer.data)
    
class SalesSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start = request.query_params.get("start")
        end = request.query_params.get("end")

        # Validate required params
        if not start or not end:
            return Response(
                {"error": "start and end are required. Format: YYYY-MM-DD"},
                status=400
            )

        # Parse dates
        try:
            start_date = datetime.strptime(start, "%Y-%m-%d").date()
            end_date = datetime.strptime(end, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD"},
                status=400
            )

        # Validate date order
        if end_date < start_date:
            return Response(
                {"error": "end must be greater than or equal to start"},
                status=400
            )

        qs = SaleInvoice.objects.filter(created_at__date__range=[start_date, end_date])

        summary = qs.aggregate(
            total_invoices=Count("id"),
            total_sales=Sum("total_amount"),
        )

        return Response({
            "start": start,
            "end": end,
            "total_invoices": summary["total_invoices"],
            "total_sales": str(summary["total_sales"] or 0),
        })


class TopProductView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # limit param safe parsing
        try:
            limit = int(request.query_params.get("limit", 10))
        except ValueError:
            limit = 10

        # optional: max limit safety
        if limit > 50:
            limit = 50
        if limit <= 0:
            limit = 10

        qs = (
            SaleItem.objects.values("product", "product__name")
            .annotate(
                total_qty_sold=Sum("qty"),
                total_revenue=Sum("line_total"),
            )
            .order_by("-total_qty_sold")[:limit]
        )

        results = [
            {
                "product_id": row["product"],
                "product_name": row["product__name"],
                "total_qty_sold": row["total_qty_sold"] or 0,
                "total_revenue": str(row["total_revenue"] or 0),
            }
            for row in qs
        ]

        return Response({
            "limit": limit,
            "results": results
        })



class profitView(APIView):
    permission_classes=[IsAuthenticated]   
    def get(self , request)  :
        start_date=request.query_params.get("start")   
        end_date=request.query_params.get("end")

        if not start_date or not end_date:
            return Response(
               { "error" : "start and end date is required . formate is YYYY-MM-DD"},
               status=400
            )
        
        try:
            start_date=datetime.strptime(start_date , "%Y-%m-%d").date()
            end_date=datetime.strptime(end_date , "%Y-%m-%d").date()
        except :
            return Response(
                { "error" : "Invalid formate . formate is YYYY-MM-DD"},
               status=400
            )
        
        if end_date<start_date:
            return Response(
                {"error" : "end date must be greater then start date "},
                status=400
            )
        qs = SaleItem.objects.filter(
             invoice__created_at__date__range=[start_date, end_date]
           )
        # print(qs)
        revenue = qs.aggregate(revenue=Sum("line_total"))["revenue"] or 0
        cost_expr = ExpressionWrapper(
            F("qty") * F("product__cost_price"),
            output_field=DecimalField(max_digits=15, decimal_places=2)
        )
        estimated_cost = qs.aggregate(cost=Sum(cost_expr))["cost"] or 0
        profit=revenue-estimated_cost
        return Response(
            {
                "start": start_date,
                "end": end_date,
                "revenue":str(revenue),
                "estimated_cost" : str(estimated_cost),
                "profit" :str(profit)
            }
        )


class CustomerLedgerView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self , request):
        customer_id=request.query_params.get("customer")
        if not customer_id:
            return Response({
                "error" : "Customer Id is requered..."
            } , status=400)
        customer = get_object_or_404(Customer, id=customer_id)
        invoice=SaleInvoice.objects.filter(customer=customer).order_by("-created_at")
        
        invoice_list=[]
        total_sale=0
        total_paid=0
        total_due=0

        for i in invoice:
            paid=i.payments.aggregate(total=Sum("amount"))["total"] or 0
            due=i.total_amount-paid
            invoice_list.append({
                "id":i.id,
                "invoice_no":i.invoice_no,
                "date":str(i.created_at.date()),
                "total_amount":str(i.total_amount),
                "paid":str(paid),
                "due":str(due),
                "starus":i.payment_status
            })
            
            total_sale+=i.total_amount
            total_paid+=paid
            total_due+=due
        return Response({
            "customer_id":customer_id,
            "customer_name":customer.name,
            "summary":{
                "total_invoices": invoice.count(),
                "total_sale":str(total_sale),
                "total_paid":str(total_paid),
                "total_due":str(total_due)
            },
            "invoice_list":invoice_list
        }

    )   



class SupplierLedgerView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self , request):
        supplier_id=request.query_params.get("supplier")
        if not supplier_id:
            return Response({
                "error":"supplier id is require"
            })
        supplier_id=get_object_or_404(Supplier ,id=supplier_id)
        invoice=PurchaseInvoice.objects.filter(supplier=supplier_id).order_by("-created-at")

        invoice_list=[]
        total_sale=0
        total_paid=0
        total_due=0

        for i in invoice:
            paid=i.payments.aggregate(total=Sum("amount"))["total"] or 0
            due=i.total_amount-paid
            invoice_list.append({
                "id":i.id,
                "invoice_no":i.invoice_no,
                "date":str(i.created_at.date()),
                "total_amount":str(i.total_amount),
                "paid":str(paid),
                "due":str(due),
                "starus":i.payment_status
            })
            
            total_sale+=i.total_amount
            total_paid+=paid
            total_due+=due
        return Response({
            "supplier_id":supplier_id,
            "supplier_name":Supplier.name,
            "summary":{
                "total_invoices": invoice.count(),
                "total_sale":str(total_sale),
                "total_paid":str(total_paid),
                "total_due":str(total_due)
            },
            "invoice_list":invoice_list
        }

    )              







