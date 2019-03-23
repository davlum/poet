import app.controllers.util as u
import app.controllers.work as work
from app.models.choices import PUBLISHED


def get_entity(entity_id: int):
    q = """
    SELECT * 
    FROM poet_entity e
    WHERE e.id = %s AND e.release_state = %s"""

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


def get_affiliated_entities(entity_id: int):
    q = """
    SELECT * 
    FROM poet_entity e
    
    """

def get_recordings(entity_id: int):
    q = """
    SELECT {}
    FROM poet_entity_to_work_rel rel
    JOIN poet_work w ON rel.to_work = w.id
    JOIN poet_work_collection c ON c.id = w.in_collection
    AND rel.from_entity = %s
    AND w.release_state = %s""".format(work.REQUIRED_WORK_FIELDS)

    recordings = u.query(q, [entity_id, PUBLISHED])
    return list(map(work.enrich_work, recordings))


def enrich_entity(entity):
    return {
        'entity': clean_entity(entity),
        'works': get_recordings(entity['id']),
        'affiliates': get_affiliated_entities(entity['id'])
    }


def get_entity_context(entity_id: int):
    entity = get_entity_or_404(entity_id)
    return enrich_entity(entity)
