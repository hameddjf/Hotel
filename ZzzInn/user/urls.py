from rest_framework.routers import DefaultRouter

from django.urls import path, include

from . import views

router = DefaultRouter()
router.register(r'hotel-staff', views.HotelStaffViewSet)
router.register(r'hotel-admin', views.HotelAdminViewSet)

urlpatterns = [
    path('users/create/', views.UserCreateAPIView.as_view(),
         name='user-create'),
    path('users/<int:pk>/update/', views.UserUpdateAPIView.as_view(),
         name='user-update'),
    path('api/token/', views.ObtainAuthTokenAPIView.as_view(),
         name='api-token'),
    path('customer/', views.CustomerUserView.as_view(),
         name='customer-detail'),

    path('', include(router.urls)),
]
