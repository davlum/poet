from django.shortcuts import get_object_or_404
from poet.entities.util import query, get_roles, render_name_link
from poet.models.work import Work
from poet.models.relations import INTERPRETERS, COMPOSERS


def get_entities(work_id):
    q = """
    SELECT 
        from_entity_id,
        role_id
    FROM poet_entity_to_work_rel rel 
    WHERE rel.to_work_id = %s
    """
    return query(q, [work_id])


def categorize_entities(work_id):
    entities = get_entities(work_id)
    entities = list(map(lambda e: {'link': render_name_link(e['from_entity_id']), **e}, entities))
    composers = [i for i in entities if i['role_id'] in get_roles(COMPOSERS)]
    interpreters = [i for i in entities if i['role_id'] in get_roles(INTERPRETERS)]
    others = [i for i in entities if i['role_id'] not in (get_roles(INTERPRETERS) + get_roles(COMPOSERS))]
    return {
        'composers': composers,
        'interpreters': interpreters,
        'others': others
    }


def get_work_context(work_id):
    return {
        'work': get_object_or_404(Work, pk=work_id),
        **categorize_entities(work_id)
    }
