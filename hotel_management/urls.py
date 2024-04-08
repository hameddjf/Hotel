from django.urls import path
from .views import rooms_list, room_detail

app_name = 'hotel'

urlpatterns = [
    path('rooms/', rooms_list, name='rooms_list'),
    path('rooms/<int:room_id>/', room_detail, name='room_detail'),
    path('search/', search, name='search'),
