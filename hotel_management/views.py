from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Room
from django.db.models import Q


def rooms_list(request):
    rooms = Room.objects.all()
    return render(request, 'hotel/room_list.html', {'rooms': rooms})


def room_detail(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    return render(request, 'hotel/room_detail.html', {'room': room})


def search(request):
    rooms = None
    if 'query' in request.GET:
        query = request.GET['query']
        rooms = Room.Available.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return render(request, 'hotel/search.html', {'rooms': rooms})
    


def room_reserve(request):
    pass


