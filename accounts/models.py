from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    STATUS_CHOICES=(
        ("OWNER", "Owner"),
        ("STAFF", "Staff"),    
    )
    email=models.EmailField(unique=True)
    status=models.CharField(max_length=20, choices=STATUS_CHOICES, default="STAFF")