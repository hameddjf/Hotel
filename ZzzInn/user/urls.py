from django.urls import path
from . import views

urlpatterns = [
    path('users/create/', views.UserCreateAPIView.as_view(),
         name='user-create'),
    path('users/<int:pk>/update/', views.UserUpdateAPIView.as_view(),
         name='user-update'),
    path('api/token/', views.ObtainAuthTokenAPIView.as_view(),
         name='api-token'),
    path('customer/profile/', views.CustomerUserView.as_view(),
         name='customer-profile'),
]
