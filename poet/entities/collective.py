from poet.entities.util import query
from poet.entities.recording import get_composition
from poet.models.models import Grupo


def get_collective_context(part_id):
    return {
        'performances': get_collectives_performances(part_id),
        'compositions': get_collectives_compositions(part_id),
        'collective': Grupo.objects.filter(part_id=part_id).filter(estado='PUBLICADO')[0],
        'artists': get_collectives_artists(part_id)
    }


def get_collectives_compositions(part_id):
    query_string = """
SELECT c.id
FROM grupo g
JOIN participante_composicion pc
  ON pc.part_id = g.part_id
JOIN composicion c
  ON c.id = pc.composicion_id  
WHERE g.part_id = %s
AND c.estado = 'PUBLICADO'
"""
    compositions = query(query_string, [part_id])
    return [get_composition(comp['id']) for comp in compositions]


def get_collectives_artists(part_id):
    query_string = """
SELECT
  p.part_id
, p.nom_part
, p.nom_paterno
, p.nom_materno
, p.fecha_comienzo
, p.fecha_finale
, p.seudonimo
, a.country_of_origin
FROM grupo a
JOIN persona_grupo pa
  ON a.part_id = pa.grupo_id
JOIN persona p
  ON p.part_id = pa.persona_id
WHERE a.part_id = %s
AND p.estado = 'PUBLICADO'
    """

    return query(query_string, [part_id])


def get_collectives_performances(part_id):
    query_string = """
SELECT DISTINCT
   c.id
FROM grupo g
JOIN participante_pista_son pps
  ON g.part_id = pps.part_id
JOIN pista_son ps
  ON ps.pista_son_id = pps.pista_son_id
JOIN composicion c
  ON c.id = ps.composicion_id
WHERE g.part_id = %s
  AND c.estado = 'PUBLICADO'
  AND (pps.rol_pista_son = 'Interpretación musical' 
  OR pps.rol_pista_son = 'Lectura en voz alta')   
    """
    compositions = query(query_string, [part_id])
    return [get_composition(comp['id']) for comp in compositions]

