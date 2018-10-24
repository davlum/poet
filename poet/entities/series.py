from poet.entities.util import query
from poet.entities.composition import get_composition
from poet.models.models import Serie


def get_series_context(series_id):
    return {
        'series': Serie.objects.get(id=series_id),
        'compositions': get_series_compositions(series_id),
        'albums': get_series_albums(series_id)
    }


def get_series_compositions(series_id):
    query_string = """
SELECT DISTINCT
  c.id
FROM composicion c
JOIN pista_son ps
ON ps.composicion_id = c.id  
WHERE ps.serie_id = %s
AND ps.estado = 'PUBLICADO' 
"""
    compositions = query(query_string, [series_id])
    return [get_composition(comp['id']) for comp in compositions]


def get_series_albums(part_id):
    query_string = """
SELECT *   
FROM album 
WHERE serie_id = %s
    """
    return query(query_string, [part_id])

