
from rest_framework import serializers
from .models import CustomUser, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

