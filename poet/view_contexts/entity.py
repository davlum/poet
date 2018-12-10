import poet.view_contexts.util as u
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from poet.models.entity import Entity


def get_recordings(entity_id: int):
    q = """
    SELECT 
        track.id,
        track.full_name,
        track.alt_name,
        track.date_recorded,
        track.file_type,
        track.path_to_file
    FROM poet_entity_to_work_rel rel
    JOIN poet_work track ON rel.to_work = track.id
    WHERE track.work_type = 'Pista son'
    AND rel.from_entity = %s
    """
    return u.query(q, [entity_id])


def get_entitys_recordings(entity_id: int):
    recordings = get_recordings(entity_id)
    cleaned_recordings = [{k: u.to_none(v) for k, v in entry.items()} for entry in recordings]
    return list(map(u.enrich_work, cleaned_recordings))


def get_entity_context(entity_id: int) -> u.Context:
    entity = model_to_dict(get_object_or_404(Entity, pk=entity_id))

    # filter empty string to none values
    cleaned_entity = {k: u.to_none(v) for k, v in entity.items()}

    location_entity = {
        **cleaned_entity,
        'location': u.get_string_location(cleaned_entity),
        'dates': u.get_dashed_date(cleaned_entity)
    }

    return u.Context(
        data={
            'entity': location_entity,
            'recordings': get_entitys_recordings(cleaned_entity['id'])
        },
        template='poet/entity.html.j2'
    )
