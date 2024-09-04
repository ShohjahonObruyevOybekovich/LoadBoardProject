
from rest_framework import serializers
from .models import CustomUser, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
class ProductUpdateSerializer(serializers.ModelSerializer):
    user = serializers.UUIDField(source='user.uuid', read_only=True)
    user_uuid = serializers.UUIDField(write_only=True, required=False)  # Optional field for admin use

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'places', 'view', 'cube', 'kg', 'cube_kg', 'price',
            'payment', 'debt', 'where_from', 'date', 'transport', 'current_place',
            'status', 'user', 'user_uuid'
        ]

class ProductCreateSerializer(serializers.ModelSerializer):
    user = serializers.UUIDField(source='user.uuid', read_only=True)
    user_uuid = serializers.UUIDField(write_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'places', 'view', 'cube', 'kg', 'cube_kg', 'price',
            'payment', 'debt', 'where_from', 'date', 'transport', 'current_place',
            'status', 'user', 'user_uuid'
        ]

    def create(self, validated_data):
        user_uuid = validated_data.pop('user_uuid')
        user = CustomUser.objects.get(uuid=user_uuid)
        product = Product.objects.create(user=user, **validated_data)
        return product