from rest_framework import serializers
from account.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            'name',
            'email',
            'password',
            'user_type',
            'account_number',
            'is_confirm',
            'is_esia_confirm',
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


class RegistrationUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        required=True,
        max_length=128,
        min_length=8,
        write_only=True
    )

    confirm_password = serializers.CharField(
        required=True,
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('name', 'email', 'user_type', 'password', 'confirm_password')

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError({'password': 'Пароли не совпадают'})

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserPasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, max_length=128, min_length=8)
    new_password = serializers.CharField(required=True, max_length=128, min_length=8)
    confirm_password = serializers.CharField(required=True, max_length=128, min_length=8)

    def validate(self, attrs):
        if not self.context['request'].user.check_password(attrs.get('old_password')):
            raise serializers.ValidationError({'old_password': 'Неверный пароль'})

        if attrs.get('new_password') != attrs.get('confirm_password'):
            raise serializers.ValidationError({'new_password': 'Пароли не совпадают'})

        if attrs.get('old_password') == attrs.get('new_password'):
            raise serializers.ValidationError({'new_password': 'Введенный пароль совпадает с текущим'})

        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance

    def create(self, validated_data):
        pass

