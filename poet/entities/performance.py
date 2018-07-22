from poet.entities.util import query_one, query


def get_performance_context(performance_id):
    return {
        'performance': get_performance(performance_id),
        'genres': get_genres(performance_id),
        'instruments': get_instruments(performance_id)
    }


def get_performance(performance_id):
    query_string = """
SELECT DISTINCT ON (a.id)
  a.pista_son_id
, a.nom_archivo
, a.id
, a.codec
, ps.pista_son_id
, ps.coment_pista_son
, ps.fecha_grab
, l.ciudad
, l.subdivision
, l.pais
, s.nom
, s.id serie_id
FROM pista_son ps
JOIN archivo a
  ON a.pista_son_id = ps.pista_son_id
LEFT JOIN serie s
  ON s.id = ps.serie_id
LEFT JOIN lugar l
  ON l.id = ps.lugar_id
WHERE ps.pista_son_id = %s
  AND ps.estado = 'PUBLICADO' 
    """
    return query_one(query_string, [performance_id])


def get_genres(performance_id):
    query_string = """
SELECT 
  g.nom
, g.id 
FROM genero_musical g
JOIN genero_pista gp
 ON g.id = gp.gen_mus_id
 WHERE gp.pista_son_id = %s
    """
    return query(query_string, [performance_id])


def get_instruments(performance_id):
    query_string = """
SELECT 
  g.part_id gr_id
, p.part_id pers_id 
, g.nom_part nom_part_ag
, p.nom_part
, p.seudonimo
, p.nom_paterno
, p.nom_materno
, i.nom nom_inst
, pps.rol_pista_son                         
FROM participante_pista_son pps
LEFT JOIN persona p
  ON p.part_id = pps.part_id
LEFT JOIN grupo g
  ON g.part_id = pps.part_id     
JOIN instrumento i
  ON i.id = pps.instrumento_id     
WHERE pps.pista_son_id= %s
    """
    return query(query_string, [performance_id])

