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
    work_dict['name'] = u.get_dashed_name(work_dict)
    return work_dict


def get_recording_entities(work_id: int) -> List[Dict[str, str]]:

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


def get_work_context(work_id: int) -> u.Context:
    work = get_work_or_404(work_id)
    return u.Context(
        data={
            'work': add_media_url_to_path(work),
            'entity': clean_recording_entities(get_recording_entities(work['id']))
        },
        template='poet/recording.html.j2'
    )
