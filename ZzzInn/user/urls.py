from django.urls import path
from . import views

urlpatterns = [

    path('', views.Checklogin, name="checklogin"),
    path('register', views.register, name="register"),
    path('login', views.Login, name="login"),
    path('logout', views.Logout, name="logout"),
    path('index', views.Index, name="index"),
    path('delete_account', views.Delete_Account, name="delete"),
]
