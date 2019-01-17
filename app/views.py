from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app.controllers.work import get_work_context
from app.controllers.search import get_search_context
from app.controllers.entity import get_entity_context
from app.controllers.collection import get_work_collection_context


def paginate_list(request, page_list, number_of_pages=10):
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
    admin_link = '/admin/app/work/{}/change'.format(work_id)
    context['admin_link'] = admin_link

    return render(request, 'poet/work.html.j2', context)


def collection(request, collection_id):
    context = get_work_collection_context(collection_id)
    admin_link = '/admin/app/workcollection/{}/change'.format(collection_id)
    context['admin_link'] = admin_link
    context['works'] = paginate_list(request, context['works'])

    return render(request, 'poet/collection.html.j2', context)


def entity(request, entity_id):
    context = get_entity_context(entity_id)
    admin_link = '/admin/app/entity/{}/change'.format(entity_id)
    context['admin_link'] = admin_link
    context['works'] = paginate_list(request, context['works'])

    return render(request, 'poet/entity.html.j2', context)


def search(request):
    context = get_search_context(dict(request.GET))
    context['works'] = paginate_list(request, context['works'])

    return render(request, 'poet/search.html.j2', context)


def error_404_view(request, _):
    return render(request, 'errors/404.html.j2')