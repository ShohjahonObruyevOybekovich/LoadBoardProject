from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from django.contrib.auth import get_user_model, authenticate
from rest_framework.serializers import ModelSerializer

from .models import CustomUser

User = get_user_model()



class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username','password','role')


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)
    role = serializers.CharField(max_length=50)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        role = attrs.get('role')


        if username and password and role:

            user = authenticate(request=self.context.get('request'), username=username, password=password, role=role)
            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs




class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True, required=False)
    role = serializers.CharField(max_length=50)

    class Meta:
        model = User
        fields = ['username', 'password','role']

    def update(self, instance, validated_data):

        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)
#
class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['uuid','username', 'role']
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ( 'uuid','username',  'role')