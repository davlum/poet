from django.shortcuts import render
from poet.entities.artist import get_artist_context
from poet.entities.composition import get_composition_context
from poet.entities.collective import get_collective_context
from poet.entities.series import get_series_context
from poet.entities.search import get_search_context
from poet.urls import Entities


def artist(request, artist_id):
    return render(request, 'poet/artist.html', get_artist_context(artist_id))


def collective(request, artist_id):
    return render(request, 'poet/collective.html', get_collective_context(artist_id))


def composition(request, composition_id):
    return render(request, 'poet/composition.html', get_composition_context(composition_id))


def series(request, series_id):
    return render(request, 'poet/series.html', get_series_context(series_id))


def search(request, entity_name=Entities.ALL.value):
    return render(request, 'poet/search.html', get_search_context(entity_name))


def index(request):
    return render(request, 'poet/index.html')


def home(request):
    return render(request, 'poet/home.html')


