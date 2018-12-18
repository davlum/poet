import app.view_contexts.util as u
from app.models.choices import PUBLISHED
from typing import Dict, List
from django.conf import settings
import os


def get_work(work_id: int):
    q = """SELECT * FROM poet_work WHERE id = %s AND release_state = %s"""

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

