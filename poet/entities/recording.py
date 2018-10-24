from poet.entities.util import query, get_or_404
from poet.entities.performance import get_performance_context
from poet.models.models import Idioma, Tema, PistaSon


def get_composition_context(comp_id):
    composition = get_composition(comp_id)
    # Make sure the composition exists
    get_or_404(composition)

    themes = Tema.objects.filter(temacomposicion__composicion_id=comp_id)
    languages = Idioma.objects.filter(idiomacomposicion__composicion_id=comp_id)

    return {
        'composition': composition,
        'languages': languages,
        'themes': themes,
        'performances': get_compositions_performances(comp_id)
    }


def get_composition(comp_id):
    """
    :param comp_id:
    :return: a list of [{comp, artist_1},
                        {comp, artist_2}]
    """
    query_string = """
SELECT DISTINCT ON (p.part_id, g.part_id)
  c.id comp_id
, c.nom_tit
, p.part_id pers_id
, g.part_id gr_id
, c.nom_alt
, c.fecha_pub
, c.texto
, g.nom_part nom_part_ag
, p.nom_part
, pc.rol_composicion
, ps.numero_de_pista
, p.seudonimo
, p.nom_paterno
, p.nom_materno
, s.id serie_id
, s.ruta_foto
, s.nom
, cobl.licencia_cobertura
FROM composicion c
JOIN participante_composicion pc
  ON c.id = pc.composicion_id
LEFT JOIN pista_son ps
  ON ps.composicion_id = c.id
LEFT JOIN serie s
  ON s.id = ps.serie_id   
LEFT JOIN persona p
  ON p.part_id = pc.part_id
LEFT JOIN grupo g
  ON g.part_id = pc.part_id
LEFT JOIN cobertura cob
  ON cob.composicion_id = c.id
JOIN cobertura_licencia cobl
  ON cobl.id = cob.cobertura_lic_id  
WHERE c.id = %s 
AND c.estado = 'PUBLICADO' 
"""
    return query(query_string, [comp_id])


def get_compositions_performances(comp_id):
    return [get_performance_context(perf.pista_son_id) for perf in PistaSon.objects.filter(composicion_id=comp_id)]

