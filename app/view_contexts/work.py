import poet.view_contexts.util as u
from poet.models.relations import COMPOSER, READER, MUSICIAN
from poet.models.choices import PUBLISHED
from typing import Dict, List
from django.conf import settings
import os


def get_work(work_id: int):
    q = """SELECT * FROM poet_work WHERE id = %s AND release_state = %s"""

    work = u.query(q, [work_id, PUBLISHED])[0]

    return {k: u.to_none(v) for k, v in work.items()}


def get_work_or_404(work_id):
    return u.return_or_404(get_work, work_id=work_id)


def add_media_url_to_path(work_dict):
    file_path = os.path.join(settings.MEDIA_URL, work_dict['audio'])
    work_dict['audio'] = file_path
    work_dict['work_name'] = u.get_dashed_name(work_dict)
    return work_dict


def get_recording_entities(work_id: int) -> List[Dict[str, str]]:

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

    return u.query(q, [work_id, PUBLISHED])


def clean_recording_entities(entity_ls: List[Dict[str, str]]):
    composers = [i for i in entity_ls if i['relationship'] == COMPOSER]
    interpreters = [i for i in entity_ls if i['relationship'] in [READER, MUSICIAN]]
    others = [i for i in entity_ls if i['relationship'] not in [READER, MUSICIAN, COMPOSER]]
    return {
        'composers': composers,
        'interpreters': interpreters,
        'others': others
    }


def get_work_context(work_id: int):
    work = get_work_or_404(work_id)
    return {
        'work': add_media_url_to_path(work),
        'entities': clean_recording_entities(get_recording_entities(work['id']))
    }
