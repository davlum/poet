from enum import Enum


class Entities(Enum):
    ALL = 'all'
    AUTHOR = 'autor'
    COLLECTIVE = 'colectivo'
    COMPOSITION = 'composicion'
    SERIES = 'serie'
    THEME = 'tema'
    GENRES = 'genero'
    INSTRUMENT = 'instrumento'
    LANGAUGE = 'idioma'
    PERFORMANCE = 'interp'
    USER = 'usuario'
    CITY = 'ciudad'
    SUBDIVISION = 'subdivision'
    COUNTRY = 'pais'


def get_search_context(search_type):
    pass