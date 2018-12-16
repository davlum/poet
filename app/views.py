from django.shortcuts import render
from poet.view_contexts.work import get_work_context
from poet.view_contexts.search import get_search_context
from poet.view_contexts.entity import get_entity_context
from poet.view_contexts.work_collection import get_work_collection_context


def index(request):
    return render(request, 'poet/index.html.j2')


def home(request):
    return render(request, 'poet/home.html.j2')


def work(request, work_id):
    context = get_work_context(work_id)
    return render(request, 'poet/work.html.j2', context)


def work_collection(request, work_collection_id):
    context = get_work_collection_context(work_collection_id)
    return render(request, 'poet/work_collection.html.j2', context)


def entity(request, entity_id):
    context = get_entity_context(entity_id)
    return render(request, 'poet/entity.html.j2', context)


def search(request):
    search_term = request.GET.get('term', '')
    context = get_search_context(search_term)
    return render(request, 'poet/search.html.j2', context)




