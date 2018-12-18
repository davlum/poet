from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app.view_contexts.work import get_work_context
from app.view_contexts.search import get_search_context
from app.view_contexts.entity import get_entity_context
from app.view_contexts.collection import get_work_collection_context


def paginate_list(request, page_list, number_of_pages):
    paginator = Paginator(page_list, number_of_pages)
    page = request.GET.get('page', 1)
    get_copy = request.GET.copy()
    parameters = get_copy.pop('page', True) and get_copy.urlencode()

    try:
        p = paginator.page(page)
    except PageNotAnInteger:
        p = paginator.page(1)
    except EmptyPage:
        p = paginator.page(paginator.num_pages)

    return {
        'page': p,
        'search_terms': parameters,
    }


def index(request):
    return render(request, 'poet/index.html.j2')


def home(request):
    return render(request, 'poet/home.html.j2')


def work(request, work_id):
    context = get_work_context(work_id)
    return render(request, 'poet/work.html.j2', context)


def collection(request, collection_id):
    context = get_work_collection_context(collection_id)
    context['works'] = paginate_list(request, context['works'], 5)

    return render(request, 'poet/collection.html.j2', context)


def entity(request, entity_id):
    context = get_entity_context(entity_id)
    context['works'] = paginate_list(request, context['works'], 5)

    return render(request, 'poet/entity.html.j2', context)


def search(request):
    search_term = request.GET.get('term', '')
    recording_list = get_search_context(search_term)
    context = paginate_list(request, recording_list, 10)

    return render(request, 'poet/search.html.j2', context)

