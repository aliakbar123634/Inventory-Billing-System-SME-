from django.urls import path
from accounts import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("auth/register/", views.RegisterOwnerView.as_view()),
    path("auth/login/", views.EmailTokenObtainPairView.as_view(), name="email-login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("staff/create/", views.StaffCreateView.as_view(), name="staff-create"),
]
