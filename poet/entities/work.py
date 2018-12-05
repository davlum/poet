from django.shortcuts import get_object_or_404
import poet.entities.util as u
from django.forms.models import model_to_dict
from poet.models.work import Work, SERIES, RECORDING
from poet.models.relations import COMPOSER, READER, MUSICIAN
from typing import Dict, List
from pampy import match, _


def get_recording_entities(work_id: int) -> List[Dict[str, str]]:
    # TOMORROW, DO YOU WANT TO RELATE SERIES AND ENTITIES

    q = """
    SELECT DISTINCT
        en.id,
        en.full_name,
        en.alt_name,
        rel.relationship
    FROM poet_entity_to_work_rel rel
    JOIN poet_entity en ON en.id = rel.from_entity
    WHERE rel.to_work = %s
    """
    return u.query(q, [work_id])


def get_series_entities(work_id: int) -> List[Dict[str, str]]:
    # TOMORROW, DO YOU WANT TO RELATE SERIES AND ENTITIES

    q = """
    SELECT DISTINCT
        en.id,
        en.full_name,
        en.alt_name,
        etw.relationship
    FROM poet_entity_to_work_rel etw
    JOIN poet_entity en ON en.id = etw.from_entity
    JOIN poet_work track ON track.id = etw.to_work
    JOIN poet_work_to_work_rel wtw on track.id = wtw.to_work
    JOIN poet_work series ON wtw.from_work = series.id
    WHERE series.id = %s
    AND wtw.relationship = 'series<contains>recording'
    """
    return u.query(q, [work_id])


def get_recordings(work_id: int):
    q = """
    SELECT 
        track.id,
        track.full_name,
        track.alt_name,
        track.date_recorded,
        track.file_type,
        track.path_to_file
    FROM poet_work_to_work_rel rel 
    JOIN poet_work track ON rel.to_work = track.id
    JOIN poet_work series ON rel.from_work = series.id
    WHERE series.id = %s
    AND rel.relationship = 'series<contains>recording'
    """
    return u.query(q, [work_id])


def get_series_recordings(work_id: int):
    recordings = get_recordings(work_id)
    cleaned_recordings = [{k: u.to_none(v) for k, v in entry.items()} for entry in recordings]
    return list(map(u.enrich_work, cleaned_recordings))


def clean_recording_entities(entity_ls: List[Dict[str, str]]):
    cleaned_entities = [{k: u.to_none(v) for k, v in entry.items()} for entry in entity_ls]
    entities = list(map(lambda e: {
        'name': u.get_dashed_name(e),
        **e
    }, cleaned_entities))
    composers = [i for i in entities if i['relationship'] == COMPOSER]
    interpreters = [i for i in entities if i['relationship'] in [READER, MUSICIAN]]
    others = [i for i in entities if i['relationship'] not in [READER, MUSICIAN, COMPOSER]]
    return {
        'composers': composers,
        'interpreters': interpreters,
        'others': others
    }


def get_series(work) -> u.Context:
    return u.Context(
        data={
            'work': work,
            'work_data': {
                'full_path': u.get_full_path(work),
            },
            'recordings': get_series_recordings(work['id']),
            'entity': clean_recording_entities(get_series_entities(work['id']))
        },
        template='poet/series.html.j2'
    )


def get_recording(work) -> u.Context:
    return u.Context(
        data={
            'work': work,
            'work_data': {
                'full_path': u.get_full_path(work),
                'codec': u.get_codec(work)
            },
            'entity': clean_recording_entities(get_recording_entities(work['id']))
        },
        template='poet/recording.html.j2'
    )


def get_work_context(work_id: int) -> u.Context:
    work = model_to_dict(get_object_or_404(Work, pk=work_id))
    pattern = work['work_type']

    # filter empty string to none values
    cleaned_work = {k: u.to_none(v) for k, v in work.items()}

    return match(pattern,
        SERIES, lambda _: get_series(cleaned_work),
        RECORDING, lambda _: get_recording(cleaned_work),
        _, lambda _: u.raise_(ValueError("Could not match '{}' of type '{}'".format(pattern, type(pattern))))
    )
