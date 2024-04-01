from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Room


def rooms_list(request):
    rooms = Room.objects.all()
    return render(request, 'rooms_list.html', {'rooms': rooms})


def room_detail(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    return render(request, 'room_detail.html', {'room': room})