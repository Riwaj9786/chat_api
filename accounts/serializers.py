from rest_framework import serializers
from django.contrib.auth import authenticate

from accounts.models import User


class EditUserAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('avatar',)


class EditUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('avatar', 'name')


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email').lower()
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError("Please give both email and password!")
        
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email doesn't Exist, Register yourself first to login!")
        
        user = authenticate(request=self.context.get('request'), email=email, password=password)

        if not user:
            raise serializers.ValidationError("Wrong Credentials!")
        
        attrs['user'] = user
        return attrs
    

class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': "password"})
    confirm_password = serializers.CharField(write_only=True, style={'input_type': "password"})

    class Meta:
        model = User
        fields = ('email', 'name', 'password', 'confirm_password')

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError({'password': "Passwords do not match!"})

        if len(password) < 8:
            raise serializers.ValidationError({'password': "Password must be at least 8 characters long!"})

        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user 