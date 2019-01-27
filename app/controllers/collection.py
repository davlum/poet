import app.controllers.util as u
import app.controllers.work as work
from app.models.choices import PUBLISHED
from django.conf import settings
from typing import List, Dict
import os


def get_collection(collection_id: int):
    q = """SELECT * FROM poet_work_collection WHERE id = %s AND release_state = %s"""

    return u.query(q, [collection_id, PUBLISHED])[0]


def get_collection_or_404(collection_id):
    return u.return_or_404(get_collection, collection_id=collection_id)


def clean_collection(collection_dict):
    collection_dict = {k: u.to_none(v) for k, v in collection_dict.items()}
    file_path = os.path.join(settings.MEDIA_URL, collection_dict['image'])
    collection_dict['image'] = file_path
    collection_dict['collection_id'] = collection_dict['id']
    return collection_dict


def get_recordings(collection_id: int):
    q = """
    SELECT {}
    FROM poet_work w
    JOIN poet_work_collection c ON c.id = w.in_collection
    WHERE w.in_collection = %s
    AND w.release_state = %s""".format(work.REQUIRED_WORK_FIELDS)

    recordings = u.query(q, [collection_id, PUBLISHED])
    return list(map(work.enrich_work, recordings))


def get_entities(collection_id: int) -> List[Dict[str, str]]:

    q = """
    SELECT DISTINCT
        en.id entity_id,
        join_words(en.full_name, en.alt_name) entity_name,
        rel.relationship,
        rel.instrument
    FROM poet_entity_to_work_rel rel
    JOIN poet_entity en ON en.id = rel.from_entity
    JOIN poet_work pw ON rel.to_work = pw.id
    WHERE pw.in_collection = %s
    AND en.release_state = %s
    """

    return u.sort_entities(u.query(q, [collection_id, PUBLISHED]))


def enrich_collection(collection):
    return {
        'collection': clean_collection(collection),
        'works': get_recordings(collection['id']),
        'entities': get_entities(collection['id'])
    }


def get_work_collection_context(collection_id: int):
    collection = get_collection_or_404(collection_id)
    return enrich_collection(collection)
