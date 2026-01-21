from django.shortcuts import render
from rest_framework import generics
from .serializer import *
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from .permissions import *
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class RegisterOwnerView(generics.CreateAPIView):
    serializer_class=RegisterOwnerSerializer
    permission_classes=[AllowAny]

class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class=EmailTokenObtainPairSerializer 


class StaffCreateView(generics.CreateAPIView):
    serializer_class=StaffCreateSerializer
    permission_classes=[IsAuthenticated , IsOwner]
    def create(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        staff_user = serializer.save()

        return Response(
            {
                "message": "Staff created successfully",
                "staff": {
                    "username": staff_user.username,
                    "email": staff_user.email,
                    "status": staff_user.status,
                },
                "generated_password": staff_user.generated_password
            },
            status=status.HTTP_201_CREATED
        )
        


