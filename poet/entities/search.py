from enum import Enum
from typing import List
from poet.entities.util import query
from functools import partial


class Entities(Enum):
    ALL = 'all'
    AUTHOR = 'autor'
    COLLECTIVE = 'colectivo'
    COMPOSITION = 'composicion'
    SERIES = 'serie'
    THEME = 'tema'
    GENRES = 'genero'
    INSTRUMENT = 'instrumento'
    LANGUAGE = 'idioma'
    PERFORMANCE = 'interp'
    USER = 'usuario'
    CITY = 'ciudad'
    SUBDIVISION = 'subdivision'
    COUNTRY = 'pais'


def make_field_search(field_list: List[str]):
    return ' OR '.join([
        "to_tsvector('es', {field}) @@ to_tsquery('es', CONCAT(%s, ':*'))".format(field=field) for field in field_list
    ]) + "AND estado = 'PUBlICADO'"


def search_model(model: Entities, field_list: List[str], term, join_statement=''):
    suffix = make_field_search(field_list)
    query_string = """
SELECT *
FROM {model}
{join}
WHERE {suffix}
""".format(model=model, suffix=suffix, join=join_statement)
    result = query(query_string, [term]*len(field_list))
    return result


ARTIST_FIELDS = ['nom_part', 'nom_paterno', 'nom_materno', 'seudonimo', 'coment_part', 'email', 'direccion',
                 'sitio_web']
GROUP_FEILDS = ['nom_part', 'coment_part', 'email', 'direccion', 'sitio_web']
COMPOSITION_FIELDS = ['nom_tit', 'nom_alt', 'texto']

search_artists = partial(search_model, 'persona', ARTIST_FIELDS)

search_groups = partial(search_model, 'grupo', GROUP_FEILDS)

search_compositions = partial(search_model, 'composicion', COMPOSITION_FIELDS)


def get_search_context(entity_name: Entities, search_term):
    return {
        'artists': search_artists(term=search_term)
    }