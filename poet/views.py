from django.shortcuts import render
from poet.entities.work import get_work_context
from poet.entities.search import get_search_context
from poet.urls import Entities


def work(request, work_id):
    return render(request, 'poet/work.html.j2', get_work_context(work_id))


def search(request, entity_name=Entities.ALL.value):
    search_term = request.GET.get('term', '')
    return render(request, 'poet/search.html.j2', get_search_context(entity_name, search_term))


def index(request):
    return render(request, 'poet/index.html.j2')


def home(request):
    return render(request, 'poet/home.html.j2')

