from django.shortcuts import get_object_or_404
from poet.entities.util import query, render_name_link
from poet.models.work import Work, SERIES, RECORDING
from poet.models.relations import COMPOSER, READER, MUSICIAN
from pampy import match, _


def get_entities(work_id):
    q = """
    SELECT 
        from_entity_id,
        role_id
    FROM poet_entity_to_work_rel rel 
    WHERE rel.to_work_id = %s
    """
    return query(q, [work_id])


def get_recording_entities(work_id):
    entities = get_entities(work_id)
    entities = list(map(lambda e: {'link': render_name_link(e['from_entity_id']), **e}, entities))
    composers = [i for i in entities if i['role_id'] == COMPOSER]
    interpreters = [i for i in entities if i['role_id'] in [READER, MUSICIAN]]
    others = [i for i in entities if i['role_id'] not in [READER, MUSICIAN, COMPOSER]]
    return {
        'composers': composers,
        'interpreters': interpreters,
        'others': others
    }


def get_series_(series_id):
    pass


def get_work_context(work_id):
    work = get_object_or_404(Work, pk=work_id)

    match(work.work_type,
        SERIES,
        RECORDING,
        _, ValueError('')
    )

    return {
        'work': work,
        **categorize_entities(work_id)
    }
