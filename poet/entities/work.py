from django.shortcuts import get_object_or_404
from poet.entities.util import query, render_name_link, raise_, Context
from poet.models.work import Work, SERIES, RECORDING
from poet.models.relations import COMPOSER, READER, MUSICIAN
from pampy import match, _


def get_entities(work_id: int):
    q = """
    SELECT 
        rel.from_entity_id,
        rel.relationship
    FROM poet_entity_to_work_rel rel 
    WHERE rel.to_work_id = %s
    """
    return query(q, [work_id])


def get_recordings(work_id: int):
    q = """
    SELECT 
        rel.from_entity_id,
        rel.relationship
    FROM poet_entity_to_work_rel rel 
    JOIN poet_work track ON rel.to_work_id = track.id
    JOIN poet_work_to_work_rel s_to_t ON track.id = s_to_t.to_work
    JOIN poet_work series ON series.id = s_to_t.from_work
    WHERE series.id = %s
    """
    return query(q, [work_id])


def get_work_entities(work_id: int):
    entities = get_entities(work_id)
    entities = list(map(lambda e: {'link': render_name_link(e['from_entity_id']), **e}, entities))
    composers = [i for i in entities if i['relationship'] == COMPOSER]
    interpreters = [i for i in entities if i['relationship'] in [READER, MUSICIAN]]
    others = [i for i in entities if i['relationship'] not in [READER, MUSICIAN, COMPOSER]]
    return {
        'composers': composers,
        'interpreters': interpreters,
        'others': others
    }


def get_series(work: Work) -> Context:
    return Context(
        data={
            'work': work,
            **get_work_entities(work.id),
        },
        template='poet/series.html.j2'
    )


def get_recording(work: Work) -> Context:
    return Context(
        data={
            'work': work,
            **get_work_entities(work.id),
        },
        template='poet/recording.html.j2'
    )


def get_work_context(work_id: int) -> Context:
    work = get_object_or_404(Work, pk=work_id)
    pattern = work.work_type
    return match(pattern,
        SERIES, lambda _: get_series(work),
        RECORDING, lambda _: get_recording(work),
        _, lambda _: raise_(ValueError("Could not match '{}' of type '{}'".format(pattern, type(pattern))))
    )
