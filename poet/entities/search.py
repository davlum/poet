from enum import Enum
from typing import List
from functools import partial
import poet.entities.util as u


class Entities(Enum):
    ALL = 'all'


def make_field_search(field_list: List[str]):
    return ' OR '.join([
        "to_tsvector('es', {field}) @@ to_tsquery('es', CONCAT(%s, ':*'))".format(field=field) for field in field_list
    ])


def search_model(model: Entities, field_list: List[str], term: str, join_statement='', predicate=''):
    suffix = make_field_search(field_list)
    query_string = """
    SELECT *
    FROM {model}
    {join}
    WHERE ({suffix})
    AND (release_state = 'PUBLICADO'
    {predicate})
    """.format(model=model, suffix=suffix, join=join_statement, predicate=predicate)
    return u.query(query_string, [term]*len(field_list))


SHARED_FIELDS = ['full_name', 'alt_name', 'commentary', 'city', 'country']

search_entities = partial(search_model, 'poet_entity', SHARED_FIELDS)

search_recordings = partial(search_model, 'poet_work', SHARED_FIELDS)


def get_search_context(search_term):
    return u.Context(
        data={
            'entities': search_entities(term=search_term),
            'recordings': list(map(
                u.enrich_work, search_recordings(term=search_term, predicate="AND work_type = 'Pista son'"))
            )
        },
        template='poet/search.html.j2'
    )
