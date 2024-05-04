from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import User
from .serializers import (
    AuthTokenSerializer,
    UserSerializer,
    CustomerSerializer)

# Create your views here.


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        token = serializer.validated_data['token']
        headers = self.get_success_headers(serializer.data)
        return Response({'token': token.key},
                        status=status.HTTP_201_CREATED,
                        headers=headers)


class UserUpdateAPIView(generics.UpdateAPIView):
    """
    ویوی به روز رسانی یوزر برای کاربران احراز هویت شده.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # کاربران تنها می‌توانند پروفایل خود را به روز کنند.
        return self.request.user


class ObtainAuthTokenAPIView(APIView):
    """
    ویوی دریافت توکن احراز هویت.
    """
    serializer_class = AuthTokenSerializer

    def post(self, request):
        # پردازش احراز هویت و صدور توکن.
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)


class CustomerUserView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerSerializer

    def get_object(self):
        return self.request.user.customer
