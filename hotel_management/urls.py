from django.urls import path
from .views import rooms_list, room_detail

urlpatterns = [
    path('rooms/', rooms_list, name='rooms_list'),
    path('rooms/<int:room_id>/', room_detail, name='room_detail'),
]
