from rest_framework import serializers

from django.contrib.auth import get_user_model, authenticate
from rest_framework.serializers import ModelSerializer

from .models import CustomUser

User = get_user_model()



class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username','password','role')

# class ConfirmationCodeSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     confirm_code = serializers.IntegerField()
#
#
# class PasswordResetRequestSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#
#
# class PasswordResetLoginSerializer(serializers.Serializer):
#     new_password = serializers.CharField()
#


from account.permission import EmailAuthBackend
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

    def validate(self, attrs):
        user = self.instance  # Get the user instance
        if 'password' in attrs:
            user.set_password(attrs['password'])
            user.save()
        return attrs
#
class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['uuid','username', 'role']
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ( 'uuid','username',  'role')