from rest_framework import serializers
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate

from .models import User, Customer, HotelStaff, HotelAdmin


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


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = ['user', 'address', 'city', 'country',
                  'check_in', 'check_out', 'guests_number',
                  'national_code', 'loyalty_points', 'preferences',
                  'satisfaction_level', 'special_requests',
                  'reservation_status', 'payment_status',
                  'room_number', 'vip_status']
        depth = 1  # این گزینه برای نمایش جزییات ارتباطی استفاده می‌شود

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(
            UserSerializer(), validated_data=user_data)
        customer = Customer.objects.create(user=user, **validated_data)
        return customer

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user

        user.email = user_data.get('email', user.email)
        user.full_name = user_data.get('full_name', user.full_name)
        # برای به روز رسانی رمز عبور، باید از روش set_password استفاده کنیم
        password = user_data.get('password')
        if password:
            user.set_password(password)
        user.save()

        instance.address = validated_data.get('address', instance.address)
        instance.save()

        return instance


class HotelStaffSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = HotelStaff
        fields = [
            'user', 'address', 'role', 'working_hours',
            'start_date', 'department', 'emergency_contact'
        ]
        read_only_fields = ['user']


class HotelAdminSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = HotelAdmin
        fields = [
            'user', 'department', 'start_date', 'can_approve_transactions',
            'can_modify_policies', 'can_handle_complaints',
            'biography', 'advanced_training_completed'
        ]
        read_only_fields = ['user']
