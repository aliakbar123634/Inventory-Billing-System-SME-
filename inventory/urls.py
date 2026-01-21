from django.urls import include, path 
from . import views
from rest_framework.routers import DefaultRouter


router=DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'suppliers', views.SupplierViewSet, basename='supplier')
router.register(r'customers', views.CustomerViewSet, basename='customer')
urlpatterns = [
    path('', include(router.urls))
]


