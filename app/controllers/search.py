import app.controllers.work as work
from typing import List, Dict, Tuple
import app.controllers.util as u
from functools import reduce
from collections import defaultdict
from django.utils.translation import gettext_lazy as _
from enum import Enum
from functools import partial
import random


class SearchFields(Enum):
    WORKS = ('works', _('Recordings'))
    ENTITIES = ('entities', _('Authors'))
    TAGS = ('tags', _('Tags'))
    COLLECTIONS = ('collections', _('Collections'))
    LANGUAGES = ('languages', _('Languages'))
    LICENSES = ('licenses', _('Licenses'))
    CITIES = ('cities', _('Cities'))


def get_search_fields():
    return [field.value for field in SearchFields]


def make_tsvector(field_weight_ls: List[Tuple[str, str]]) -> str:
    """
    :param field_weight_ls: A list of tuples of the name of the field and the weight to be assigned in the search
    :return:
    """
    return ' || '.join([
        "setweight(to_tsvector('es', coalesce({field}::text,'')), '{weight}')".format(field=field, weight=weight) for
        field, weight in field_weight_ls
    ])


def make_field_search(term_number: int):
    """
    :param term_number: the number of terms we are searching for
    :return:
    """
    term_wildcards = ", ' | ', ".join(["CONCAT(%s, ':*')"] * term_number)
    return "to_tsquery('es', CONCAT({query}))".format(query=term_wildcards)


def make_query(base_string: str, field_list: List[Tuple[str, str]], term: str):
    """
    :param base_string: The string to query
    :param field_list: list of fields to search and their respective search ranking
    :param term: the string you're searching for
    :return: List of matching dicts from search
    """

    if term.strip() == '':
        return []

    terms = term.split()
    query = make_field_search(len(terms))
    text = make_tsvector(field_list)

    q = base_string.format(fields=work.REQUIRED_WORK_FIELDS, query=query, text=text)

    return u.query(q, terms)


SEARCH_WORKS = """
WITH t AS (
    SELECT id vec_id, {text} vec FROM poet_work
), c AS (
    SELECT id collection_id, collection_name, commentary
    FROM poet_work_collection
)
SELECT DISTINCT
    {fields},
    ts_rank_cd(t.vec, q) rank
FROM poet_work w, {query} q, c, t
WHERE q @@ t.vec
AND w.in_collection = c.collection_id
AND w.id = t.vec_id
AND w.release_state = 'PUBLICADO'
ORDER BY rank DESC
"""

SEARCH_COLLECTIONS = """
WITH c AS (
    SELECT id collection_id, collection_name, commentary, {text} vec 
    FROM poet_work_collection
)
SELECT DISTINCT
    {fields},
    ts_rank_cd(c.vec, q) rank
FROM poet_work w, {query} q, c
WHERE q @@ c.vec
AND w.in_collection = c.collection_id
AND w.release_state = 'PUBLICADO'
ORDER BY rank DESC
"""


SEARCH_ENTITES = """
WITH t AS (
    SELECT id vec_id, {text} vec FROM poet_entity
), c AS (
    SELECT id collection_id, collection_name
    FROM poet_work_collection
)
SELECT DISTINCT
    {fields},
    ts_rank_cd(t.vec, q) rank
FROM poet_work w, {query} q, c, t, poet_entity_to_work_rel rel
WHERE q @@ t.vec
AND rel.to_work = w.id
AND w.in_collection = c.collection_id
AND rel.from_entity = t.vec_id
AND w.release_state = 'PUBLICADO'
ORDER BY rank DESC
"""


def search_works_and_entities(field_list: List[Tuple[str, str]], term: str):
    return make_query(SEARCH_WORKS, field_list, term) + make_query(SEARCH_ENTITES, field_list, term)


class Accumulator:

    def __init__(self):
        self.collections = {}
        self.tags = defaultdict(int)
        self.licenses = defaultdict(int)
        self.cities = defaultdict(int)
        self.languages = defaultdict(int)

    def __str__(self):
        return """
        Licenses: {licenses}\n
        Cities: {countries}\n
        Tags: {tags}\n
        Collections: {collections}\n
        Languages: {languages}
        """.format(
            licenses=self.licenses,
            countries=self.cities,
            tags=self.tags,
            collections=self.collections,
            languages=self.languages
        )


def collection_counter(d: Dict[int, dict], collection_id, collection_name):
    maybe_counter = d.get(collection_id)
    if maybe_counter:
        d[collection_id]['count'] += 1
    else:
        d[collection_id] = {}
        d[collection_id]['count'] = 1
        d[collection_id]['name'] = collection_name
    return d


def dict_agg(d: defaultdict, ele: str):
    d[ele.strip().lower()] += 1
    return d


def get_aggregate_data(model_ls: List[Dict]) -> Accumulator:

    def reducer(acc: Accumulator, ele: dict) -> Accumulator:
        reduce(dict_agg, [] if ele['tags'] is None else ele['tags'], acc.tags)
        reduce(dict_agg, [] if ele['languages'] is None else ele['languages'], acc.languages)

        collection_counter(acc.collections, ele['in_collection'], ele['collection_name'])
        if ele['city'] is not None:
            acc.cities[ele['city'].strip()] += 1
        if ele['copyright'] is not None:
            acc.licenses[ele['copyright']] += 1

        return acc

    accumulator = reduce(reducer, model_ls, Accumulator())
    accumulator.tags = sort_and_scale_tags(accumulator.tags, 25)
    accumulator.licenses = shuffle_and_take_fields(accumulator.licenses, 5)
    accumulator.cities = shuffle_and_take_fields(accumulator.cities, 5)
    accumulator.languages = shuffle_and_take_fields(accumulator.languages, 5)

    accumulator.collections = shuffle_and_take_collections(accumulator.collections, 5)

    return accumulator


def shuffle_and_take_fields(field_dict: defaultdict, n: int):
    dict_ls = [{'name': tup[0], 'count': tup[1]} for tup in field_dict.items()]
    random.shuffle(dict_ls)

    return dict_ls[:n]


def shuffle_and_take_collections(collection_dict: Dict[int, dict], n: int):
    dict_ls = [{'name': tup[1]['name'], 'id': tup[0], 'count': tup[1]['count']} for tup in collection_dict.items()]
    random.shuffle(dict_ls)

    return dict_ls[:n]


def sort_and_scale_tags(d: Dict[str, int], n: int) -> List[dict]:
    top_n_tags = sorted(d.items(), key=lambda x: x[1], reverse=True)[:n]

    # Check to make sure list is not empty before indexing
    if top_n_tags:
        max_size = top_n_tags[0][1]

        # scale for font size between 5 and 25
        scale_for_font_sz = [{'name': tup[0], 'count': ((tup[1] / max_size) * 16 + 8)} for tup in top_n_tags]

        random.shuffle(scale_for_font_sz)

        return scale_for_font_sz

    return []


WORK_FIELDS = [
    ('full_name', 'A'),
    ('alt_name', 'A'),
    ('commentary', 'B'),
    ('poetry_text', 'B'),
    ('city', 'C'),
    ('country', 'C'),
    ('tags', 'C')
]

ENTITY_FIELDS = [
    ('full_name', 'A'),
    ('alt_name', 'A'),
    ('commentary', 'B'),
    ('city', 'C'),
    ('country', 'C'),
]

CITIES_FIELDS = [
    ('city', 'A'),
    ('country', 'A')
]

COLLECTION_FIELDS = [
    ('collection_name', 'A'),
    ('commentary', 'B'),
]


def get_search_context(request_dict: Dict[str, str]) -> dict:
    switch_dict = {
        SearchFields.WORKS.value[0]: partial(make_query, SEARCH_WORKS, WORK_FIELDS),
        SearchFields.ENTITIES.value[0]: partial(make_query, SEARCH_ENTITES, ENTITY_FIELDS),
        SearchFields.TAGS.value[0]: partial(make_query, SEARCH_WORKS, [('tags', 'A')]),
        SearchFields.CITIES.value[0]: partial(search_works_and_entities, CITIES_FIELDS),
        SearchFields.COLLECTIONS.value[0]: partial(make_query, SEARCH_COLLECTIONS, COLLECTION_FIELDS),
        SearchFields.LANGUAGES.value[0]: partial(make_query, SEARCH_WORKS, [('languages', 'A')]),
        SearchFields.LICENSES.value[0]: partial(make_query, SEARCH_WORKS, [('copyright', 'A')])
    }
    field_key = request_dict.get('filter', SearchFields.WORKS.value)[0]
    search_term = request_dict.get('term', [''])[0]
    field_key_stripped = field_key.strip('/')
    result = switch_dict[field_key_stripped](term=search_term)
    return {
        'works': list(map(work.enrich_work, result)),
        'metadata': get_aggregate_data(result)
    }
