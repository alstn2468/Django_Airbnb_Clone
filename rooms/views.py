from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404
from rooms.models import Room, RoomType, Amenity, Facility
from django_countries import countries


class HomeView(ListView):
    """rooms application HomeView class
    Display list of room query set

    Inherit             : ListView
    Model               : Room
    paginate_by         : 10
    paginate_orphans    : 5
    ordering            : created_at
    context_object_name : rooms
    Templates name      : rooms/rooms_list.html
    """

    model = Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created_at"
    context_object_name = "rooms"

    def dispatch(self, request, *args, **kwargs):
        try:
            return super(HomeView, self).dispatch(request, *args, **kwargs)

        except Http404:
            return redirect(reverse("core:home"))


class RoomDetail(DetailView):
    """rooms application RoomDetail Class
    Display detail of room object

    Inherit : DetailView
    Model   : Room
    """

    model = Room


def search(request):
    """rooms aplication search method
    Display list of rooms searched by city

    Params
        request : HttpRequest

    Return
        rendered rooms/search.html
    """
    return render(request, "rooms/search.html")
