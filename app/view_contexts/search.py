import app.view_contexts.work as work
from typing import List, Dict, Tuple
import app.view_contexts.util as u
from functools import reduce
from collections import defaultdict
from django.utils.translation import gettext_lazy as _
from enum import Enum
from functools import partial
import random


class SearchFields(Enum):
    WORKS = ('work', _('Recordings'))
    ENTITIES = ('entities', _('Authors'))
    TAGS = ('tags', _('Tags'))
    COLLECTIONS = ('collections', _('Collections'))
    LOCATIONS = ('locations', _('Locations'))


def get_search_fields():
    return [field.value for field in SearchFields]


def make_tsvector(field_weight_ls: List[Tuple[str, str]]) -> str:
    return ' || '.join([
        "setweight(to_tsvector('es', coalesce({field}::text,'')), '{weight}')".format(field=field, weight=weight) for
        field, weight in field_weight_ls
    ])


def make_field_search(field_weight_ls: List[Tuple[str, str]], term_number: int):
    ts_vector = make_tsvector(field_weight_ls)
    term_wildcards = ", ' | ', ".join(["CONCAT(%s, ':*')"] * term_number)
    return "to_tsquery('es', CONCAT({query}))".format(query=term_wildcards), ts_vector


def search_works(field_list: List[Tuple[str, str]], term: str):
    """

    :param field_list: list of fields to search and their respective search ranking
    :param term: the string you're searching for
    :return: List of matching dicts from search

    """

    if term.strip() == '':
        return []

    terms = term.split()
    query, text = make_field_search(field_list, len(terms))
    q = """
    WITH t AS (
        SELECT id vec_id, {text} vec FROM poet_work
    ), c AS (
        SELECT id collection_id, collection_name
        FROM poet_work_collection
    )
    SELECT 
        w.id,
        w.full_name,
        w.alt_name,
        w.city,
        w.country,
        w.languages,
        w.waveform_peaks,
        w.copyright,
        w.date_recorded, 
        w.date_published, 
        w.date_digitalized,
        w.date_contributed,
        w.tags,
        w.in_collection,
        c.collection_id,
        c.collection_name,
        w.audio,
        ts_rank_cd(t.vec, q) rank
    FROM poet_work w, {query} q, c, t
    WHERE q @@ t.vec
    AND w.in_collection = c.collection_id
    AND w.id = t.vec_id
    AND w.release_state = 'PUBLICADO'
    ORDER BY rank DESC
    """.format(query=query, text=text)

    return u.query(q, terms)


class Accumulator:

    def __init__(self):
        self.collections = {}
        self.tags = defaultdict(int)
        self.licenses = defaultdict(int)
        self.countries = defaultdict(int)

    def __str__(self):
        return "Licenses: {}\n\n Countries: {}\n\n Tags: {}\n\nCollections: {}\n\n".format(
            self.licenses,
            self.countries,
            self.tags,
            self.collections
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


def get_aggregate_data(model_ls: List[Dict]) -> Accumulator:

    def reducer(acc: Accumulator, ele: dict) -> Accumulator:
        tags = ele['tags']
        for tag in tags:
            acc.tags[tag.strip().lower()] += 1

        acc.collections = collection_counter(acc.collections, ele['in_collection'], ele['collection_name'])
        acc.countries[ele['country'].strip()] += 1
        acc.licenses[ele['copyright']] += 1

        return acc

    accumulator = reduce(reducer, model_ls, Accumulator())
    accumulator.tags = sort_and_scale_tags(accumulator.tags, 25)
    accumulator.licenses = [{'name': tup[0], 'count': tup[1]} for tup in accumulator.licenses.items()]
    accumulator.countries = [{'name': tup[0], 'count': tup[1]} for tup in accumulator.countries.items()]
    accumulator.collections = sort_and_take_collections(accumulator.collections, 5)

    return accumulator


def sort_and_take_collections(collection_dict: Dict[int, dict], n: int):
    dict_ls = [{'name': tup[1]['name'], 'id': tup[0], 'count': tup[1]['count']} for tup in collection_dict.items()][:n]
    random.shuffle(dict_ls)

    return dict_ls


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


SHARED_FIELDS = [
    ('full_name', 'A'),
    ('alt_name', 'A'),
    ('commentary', 'B'),
    ('city', 'B'),
    ('country', 'B'),
    ('tags', 'C')
]

LOCATIONS_FIELDS = [
    ('city', 'A'),
    ('country', 'A')
]


def get_search_context(request_dict: Dict[str, str]) -> dict:
    switch_dict = {
        SearchFields.WORKS.value[0]: partial(search_works, SHARED_FIELDS),
        # SearchFields.ENTITIES.value[0]: search_entities,
        SearchFields.TAGS.value[0]: partial(search_works, [('tags', 'A')]),
        SearchFields.LOCATIONS.value[0]: partial(search_works, LOCATIONS_FIELDS),
        SearchFields.COLLECTIONS.value[0]: partial(search_works, ([('collection_name', 'A')]))
    }
    field_key = request_dict.get('filter-field', [SearchFields.WORKS.value])[0]
    search_term = request_dict.get('term', [''])[0]
    result = switch_dict[field_key](term=search_term)
    return {
        'works': list(map(work.enrich_work, result)),
        'metadata': get_aggregate_data(result)
    }

