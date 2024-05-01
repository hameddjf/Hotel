from rest_framework import serializers
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """.سریال ساز برای کاربر"""
    class Meta:
        model = User
        fields = ['email', 'password', 'full_name']
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 8,
            }
        }

    def create(self, validated_data):
        """.ایجاد و برگدوندن یک کاربر با رمز عبور رمزنگاری شده"""
        user = User.objects.create_user(**validated_data)
        token, created = Token.objects.get_or_create(user=user)
        return token

    def update(self, instance, validated_data):
        """.به روز رسانی و برگردوندن کاربر"""
        # retrieve the password from validated_data then remove password(pop)
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """.سریالایزر برای تایید کاربر"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """.تایید و احراز هویت کاربر"""
        email = attrs.get('email',)
        password = attrs.get('password',)

        if email and password:
            user = authenticate(
                request=self.context.get('request',),
                email=email,
                password=password,
            )

            if not user:
                message = '.نمیتوانید وارد شوید'
                raise serializers.ValidationError(
                    message, code='authorization')

        else:
            message = '.باید شامل نام کاربری و رمز عبور باشد'
            raise serializers.ValidationError(message, code='authorization')

        attrs['user'] = user
        return attrs
