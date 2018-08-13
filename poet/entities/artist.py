from poet.entities.util import query
from poet.entities.composition import get_composition
from poet.models import ParticipantePistaSon, Persona


def get_artist_context(part_id):
    return {
        'performances': get_artists_performances(part_id),
        'compositions': get_artists_compositions(part_id),
        'artist': Persona.objects.filter(part_id=part_id).filter(estado='PUBLICADO')[0]
    }


def get_artists_compositions(part_id):
    query_string = """
SELECT c.id
FROM persona pers
LEFT JOIN persona_grupo pa
ON pers.part_id = pa.persona_id
JOIN participante_composicion pc
ON pc.part_id = pa.grupo_id
OR pc.part_id = pers.part_id
JOIN composicion c
ON c.id = pc.composicion_id
WHERE pers.part_id = %s
AND c.estado = 'PUBLICADO'
"""
    compositions = query(query_string, [part_id])

    return [get_composition(comp['id']) for comp in compositions]


def get_artists_performances(part_id):
    query_string = """
SELECT DISTINCT
   c.id
FROM persona pers
JOIN participante_pista_son pps
  ON pers.part_id = pps.part_id
JOIN pista_son ps
  ON ps.pista_son_id = pps.pista_son_id
JOIN composicion c
  ON c.id = ps.composicion_id
WHERE pers.part_id = %s
  AND c.estado = 'PUBLICADO'
  AND (pps.rol_pista_son = 'Interpretación musical' 
  OR pps.rol_pista_son = 'Lectura en voz alta')   
    """
    compositions = query(query_string, [part_id])
    return [get_composition(comp['id']) for comp in compositions]

