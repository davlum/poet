import app.controllers.util as u
from app.models.choices import PUBLISHED
from typing import Dict, List
from django.conf import settings
import os


REQUIRED_WORK_FIELDS = """
        w.id,
        w.full_name,
        w.alt_name,
        w.city,
        w.country,
        w.languages,
        w.waveform_peaks,
        w.copyright,
        w.date_recorded, 
        w.date_published, 
        w.date_digitalized,
        w.date_contributed,
        w.poetry_text,
        w.commentary,
        w.tags,
        w.in_collection,
        c.collection_name,
        w.audio
"""


def get_work(work_id: int):
    q = """
    SELECT {} 
    FROM poet_work w
    JOIN poet_work_collection c ON w.in_collection = c.id
    WHERE w.id = %s AND w.release_state = %s""".format(REQUIRED_WORK_FIELDS)

    return u.query(q, [work_id, PUBLISHED])[0]


def get_work_or_404(work_id):
    return u.return_or_404(get_work, work_id=work_id)


def clean_work(work_dict):
    work_dict = {k: u.to_none(v) for k, v in work_dict.items()}
    file_path = os.path.join(settings.MEDIA_URL, work_dict['audio'])
    work_dict['work_id'] = work_dict['id']
    work_dict['audio'] = file_path
    work_dict['work_name'] = u.get_dashed_name(work_dict)
    return work_dict


def get_entities(work_id: int) -> List[Dict[str, str]]:

    q = """
    SELECT DISTINCT
        en.id entity_id,
        join_words(en.full_name, en.alt_name) entity_name,
        rel.relationship
    FROM poet_entity_to_work_rel rel
    JOIN poet_entity en ON en.id = rel.from_entity
    WHERE rel.to_work = %s
    AND release_state = %s
    """

    return u.sort_entities(u.query(q, [work_id, PUBLISHED]))


def enrich_work(work):
    return {
        'work': clean_work(work),
        'entities': get_entities(work['id'])
    }


def get_work_context(work_id: int):
    work = get_work_or_404(work_id)
    return enrich_work(work)

