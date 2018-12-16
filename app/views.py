from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app.view_contexts.work import get_work_context
from app.view_contexts.search import get_search_context
from app.view_contexts.entity import get_entity_context
from app.view_contexts.work_collection import get_work_collection_context


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


def search_paginator(request, recording_list):
    paginator = Paginator(recording_list, 10)
    page = request.GET.get('page', 1)
    get_copy = request.GET.copy()
    parameters = get_copy.pop('page', True) and get_copy.urlencode()

    try:
        recordings = paginator.page(page)
    except PageNotAnInteger:
        recordings = paginator.page(1)
    except EmptyPage:
        recordings = paginator.page(paginator.num_pages)
    return {
        'recordings': recordings,
        'search_terms': parameters,
    }


def search(request):
    search_term = request.GET.get('term', '')
    recording_list = get_search_context(search_term)
    context = search_paginator(request, recording_list)

    return render(request, 'poet/search.html.j2', context)


def adv_search(request):
    pass

