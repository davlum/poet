
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render


def artist(request, artist_id):
    return HttpResponse("You're looking at question %s." % artist_id)


def index(request):
    return render(request, 'main/home.html')

