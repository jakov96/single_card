from django.contrib.auth import authenticate
from rest_framework import serializers
from account.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'password'
        )
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'token')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, attrs):
        email = attrs.get('email', None)
        password = attrs.get('password', None)

        if not email:
            raise serializers.ValidationError('Поле Email не может быть пустым')

        if not password:
            raise serializers.ValidationError('Поле Password не может быть пустым')

        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError('Email или пароль введены неверно')

        if not user.is_active:
            raise serializers.ValidationError('Пользователь неактивен')

        return {
            'email': user.email,
            'token': user.token
        }
