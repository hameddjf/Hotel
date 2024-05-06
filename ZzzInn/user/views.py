from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from django.http import Http404

from .models import User, HotelStaff, HotelAdmin, Customer
from .serializers import (
    AuthTokenSerializer,
    UserSerializer,
    CustomerSerializer,
    HotelStaffSerializer,
    HotelAdminSerializer)

# Create your views here.


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        # user = serializer.save()
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
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CustomerSerializer

    def get_object(self):
        try:
            return self.request.user.customer
        except Customer.DoesNotExist:
            raise Http404("مشتری یافت نشد")

    def get(self, request, *args, **kwargs):
        return super(CustomerUserView, self).get(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class HotelStaffViewSet(viewsets.ModelViewSet):
    queryset = HotelStaff.objects.all()
    serializer_class = HotelStaffSerializer

    permission_classes = [permissions.IsAuthenticated,
                          permissions.DjangoModelPermissions]

    def get_queryset(self):
        return HotelStaff.objects.filter(
            department=self.request.user.department)


class HotelAdminViewSet(viewsets.ModelViewSet):
    queryset = HotelAdmin.objects.all()
    serializer_class = HotelAdminSerializer

    permission_classes = [permissions.IsAuthenticated,
                          permissions.DjangoModelPermissions]

    def get_queryset(self):
        return HotelAdmin.objects.filter(
            department=self.request.user.department)
