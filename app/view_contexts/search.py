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
    q = """
    SELECT *
    FROM {model}
    {join}
    WHERE ({suffix})
    AND (release_state = 'PUBLICADO'
    {predicate})
    """.format(model=model, suffix=suffix, join=join_statement, predicate=predicate)

    return u.query(q, [term]*len(field_list))


def search_tags(model, term):
    result_q = """
    SELECT * 
    FROM {model}
    WHERE %s = ANY tags
    AND release_state = 'PUBLICADO'
    """.format(model=model)

    tags_q = """
    SELECT 
    tags.tags, 
    count(*) count
    FROM (
        SELECT unnest(tags) tags
        FROM {model}
        WHERE %s = ANY tags
        AND release_state = 'PUBLICADO'
    ) tags 
    GROUP BY tags.tags
    ORDER BY count DESC
    LIMIT 20; 
    """.format(model=model)

    return {
        'result': u.query(result_q, [term]),
        'tags': u.query(tags_q, [term])
    }


def get_aggregate_data():
    pass


SHARED_FIELDS = ['full_name', 'alt_name', 'commentary', 'city', 'country']

search_entities = partial(search_model, 'poet_entity', SHARED_FIELDS)

search_recordings = partial(search_model, 'poet_work', SHARED_FIELDS)


def get_search_context(request_dict: Dict[str, str]) -> List[Dict[str, str]]:
    use_tags = request_dict.get('use-tags', False)
    search_term = request_dict.get('term', '')
    if use_tags:
        result = search_tags('poet_work', search_term)
    else:
        result = search_recordings(term=search_term)
    return list(map(work.enrich_work, result))

