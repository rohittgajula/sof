from rest_framework import serializers
from .models import User
from django.db import transaction

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['otp', 'password', 'groups', 'user_permissions']


class CreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        age = serializers.ReadOnlyField()
        
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'date_of_birth', 'age']

