import app.view_contexts.util as u
import app.view_contexts.work as work
from app.models.choices import PUBLISHED


def get_entity(entity_id: int):
    q = """SELECT * FROM poet_entity WHERE id = %s AND release_state = %s"""

    return u.query(q, [entity_id, PUBLISHED])[0]


def get_entity_or_404(entity_id):
    return u.return_or_404(get_entity, entity_id=entity_id)


def clean_entity(entity_dict):
    entity_dict = {k: u.to_none(v) for k, v in entity_dict.items()}
    entity_dict['entity_id'] = entity_dict['id']
    entity_dict['entity_name'] = u.get_dashed_name(entity_dict)
    entity_dict['dates'] = u.get_dashed_date(entity_dict)
    entity_dict['location'] = u.get_dashed_location(entity_dict)
    return entity_dict


def get_recordings(entity_id: int):
    q = """
    SELECT *
    FROM poet_entity_to_work_rel rel
    JOIN poet_work track ON rel.to_work = track.id
    AND rel.from_entity = %s
    AND track.release_state = %s
    """
    recordings = u.query(q, [entity_id, PUBLISHED])
    return list(map(work.enrich_work, recordings))


def enrich_entity(entity):
    return {
        'entity': clean_entity(entity),
        'recordings': get_recordings(entity['id'])
    }


def get_entity_context(entity_id: int):
    entity = get_entity_or_404(entity_id)
    return enrich_entity(entity)
