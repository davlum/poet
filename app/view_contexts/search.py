import app.view_contexts.work as work
from typing import List, Dict
from functools import partial
import app.view_contexts.util as u


def make_field_search(field_list: List[str]):
    return ' OR '.join([
        "to_tsvector('es', {field}) @@ to_tsquery('es', CONCAT(%s, ':*'))".format(field=field) for field in field_list
    ])


def search_model(model, field_list: List[str], term: str, join_statement='', predicate=''):
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


def get_search_context(search_term: str) -> List[Dict[str, str]]:
    return list(map(work.enrich_work, search_recordings(term=search_term)))

