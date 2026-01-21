from django.urls import include, path 
from . import views
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register(r'purchase-invoices', views.PurchaseInvoiceViewSet, basename='purchase-invoice')
router.register(r'sale-invoices', views.SaleInvoiceViewSet, basename='sale-invoice')
router.register(r"sale-payments", views.SalePaymentViewset, basename="sale-payment")
router.register(r"supplier-payments", views.SupplierPaymenViewSet, basename="supplier-payment")

urlpatterns = [
    path('', include(router.urls))
]