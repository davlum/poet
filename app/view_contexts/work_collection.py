import app.view_contexts.util as u
from app.models.relations import COMPOSER, READER, MUSICIAN
from app.models.choices import PUBLISHED
from typing import Dict, List
from django.conf import settings
from functools import reduce
import os


def get_work_collection(collection_id: int):
    q = """SELECT * FROM poet_work_collection WHERE id = %s AND release_state = %s"""

    work = u.query(q, [collection_id, PUBLISHED])[0]

    return {k: u.to_none(v) for k, v in work.items()}


def get_work_collection_or_404(collection_id):
    return u.return_or_404(get_work_collection, collection_id=collection_id)


def add_media_url_to_path(collection_dict):
    file_path = os.path.join(settings.MEDIA_URL, collection_dict['images'])
    collection_dict['images'] = file_path
    return collection_dict


def get_works_from_collection(collection_id: int) -> List[Dict[str, str]]:

    q = """
    SELECT 
        w.id work_id, w.audio,
        join_words(w.full_name, w.alt_name) work_name,
        w.date_recorded,
        rel.relationship,
        e.id entity_id,
        join_words(e.full_name, e.alt_name) entity_name
    FROM poet_work w
    JOIN poet_entity_to_work_rel rel
    JOIN poet_entity e on rel.from_entity = e.id
    ON w.id = rel.to_work
    JOIN poet_entity pe on rel.from_entity = pe.id
    WHERE in_collection = %s 
    AND w.release_state = %s
    AND e.release_state = %s
    AND relationship in (%s,%s,%s)"""

    return u.query(q, [collection_id, PUBLISHED, PUBLISHED, COMPOSER, READER, MUSICIAN])


def clean_collection_recordings(recording_ls: List[Dict[str, str]]):
    cleaned_entities = [{k: u.to_none(v) for k, v in entry.items()} for entry in recording_ls]

    def reducer(dict_ls, d):
        entity = {k: d[k] for k in ('relationship', 'entity_id', 'entitiy_name')}
        if len(dict_ls) == 0 or d['work_id'] != dict_ls[-1]['work_id']:
            work = {k: d[k] for k in ('work_id', 'audio', 'work_name', 'date_recorded')}
            work['entities'] = [entity]
            file_path = os.path.join(settings.MEDIA_URL, work['audio'])
            work['audio'] = file_path
            dict_ls.append(work)
        else:
            dict_ls[-1]['entities'].append(entity)
        return dict_ls

    return reduce(reducer, cleaned_entities, [])


def get_work_collection_context(work_collection_id: int):
    work = get_work_collection_or_404(work_collection_id)
    return {
        'collection': add_media_url_to_path(work),
        'works': clean_collection_recordings(get_works_from_collection(work['id']))
    }
