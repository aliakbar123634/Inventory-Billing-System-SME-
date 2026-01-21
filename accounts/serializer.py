from rest_framework import serializers
# from .models import User 
from django.contrib.auth import get_user_model , authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .utils import generate_password




User = get_user_model()
class RegisterOwnerSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=['username' , 'email' , 'password' , 'first_name' , 'last_name']

    def validate(self , attrs):
        if User.objects.exists():
            raise serializers.ValidationError("An owner account already exists.")
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError("Username already taken.")
    
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError("Email already registered.")
        return attrs
        
    def create(self , validate_data):
        password=validate_data.pop('password')
        user=User(
            email=validate_data['email'],
            username=validate_data['username'],
            first_name=validate_data['first_name'],
            last_name=validate_data['last_name']
        )
        user.set_password(password)
        user.status = "OWNER"
        user.save()
        return user
    
        
class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field='email'  
    def validate(self , attrs):
        email=attrs.get('email')
        password=attrs.get('password')
        
        user=User.objects.filter(email=email).first()
        if not User:
            raise serializers.ValidationError("No user with this email found..")
        
        authenticate_user=authenticate(
            request=self.context.get("request"),
            username=user.username,
            password=password
        )

        if not authenticate_user:
            raise serializers.ValidationError('Invalid credentials...')
        


        refresh=self.get_token(authenticate_user)
        return{
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
    
class StaffCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username' , 'email'  , 'first_name' , 'last_name']

    def validate(self, attrs):
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError("Username already taken.")
    
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError("Email already registered.")
    
        return attrs
    

    def create(self , validate_data):
        raw_password = generate_password(10)
        user=User(
            email=validate_data['email'],
            username=validate_data['username'],
            first_name=validate_data['first_name'],
            last_name=validate_data['last_name']
        )
        user.set_password(raw_password)
        user.status = "STAFF"
        user.save()
 
 #    attach password for response
        user.generated_password=raw_password
        return user
    