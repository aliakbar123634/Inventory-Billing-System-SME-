from django.urls import  path 
from . import views



urlpatterns = [
    path('customer-ledger/' , views.CustomerLedgerView.as_view() , name='customer-ledger'),
    path('supplier-ledger/' , views.SupplierLedgerView.as_view() , name='supplier-ledger'),
    path('low-stock/' , views.LowStockProductsView.as_view() , name="low-stock"),     # http://127.0.0.1:8000/api/reports/low-stock/
    path('sales-summary/' , views.SalesSummaryView.as_view() , name="sales-summary"), #http://127.0.0.1:8000/api/reports/sales-summary/?start=2026-01-01&end=2026-01-31
    path('top-products/' , views.TopProductView.as_view() , name="top-products") ,   #
    path('profit/' , views.profitView.as_view() , name="profit")         # http://127.0.0.1:8000/api/reports/profit/?start=2026-01-01&end=2026-01-31
]
