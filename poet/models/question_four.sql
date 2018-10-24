-- OLD Top 5 interpreters with more recordings (i.e., interpretations) and total recordings per interpreter.
SELECT
   array_to_string(array_remove(ARRAY[
     p.nom_part,
     g.nom_part,
     p.seudonimo,
     p.nom_materno,
     p.nom_paterno], ''), ' ') author,
  count(DISTINCT ps.pista_son_id) recordings
FROM participante_pista_son son
LEFT JOIN persona p ON p.part_id = son.part_id
LEFT JOIN grupo g ON g.part_id = son.part_id
JOIN pista_son ps ON ps.pista_son_id = son.pista_son_id
JOIN composicion c ON c.id = ps.composicion_id
JOIN serie s ON s.id = ps.serie_id
WHERE son.rol_pista_son IN ('Lectura en voz alta', 'Interpretación musical')
AND s.nom ~* 'eslam'
GROUP BY author
ORDER BY recordings DESC
LIMIT 10;

/*
 *                 author                 | recordings
 * ---------------------------------------+------------
 *  Rojo Córdova                          |         12
 *  Luis Ro                               |          8
 *  Caco Pontes                           |          6
 *  Jonatan Huachimingo Barreda Hernández |          5
 *  Josuelfo                              |          4
 *  Renato                                |          4
 *  Kevin Kev Mara                        |          4
 *  Hugo Cóatl                            |          4
 *  Maiiky Trauma                         |          4
 *  Victoria Tyler                        |          4
 *
 */

SELECT array_to_string(array_remove(ARRAY[pe.full_name, pe.alt_name], ''), ' ') author
     , count(DISTINCT pw.id) recordings
FROM poet_entity pe
JOIN poet_entity_to_work_rel rel ON pe.id = rel.from_entity
JOIN poet_work pw ON pw.id = rel.to_work
JOIN poet_work_to_work_rel rel2 on pw.id = rel2.to_model_id
JOIN poet_work ps ON rel2.from_model_id = ps.id
WHERE rel.role_id IN ('Lectura en voz alta', 'Interpretación musical')
AND pw.work_type = 'RECORDING'
AND ps.work_type = 'SERIES'
AND ps.full_name ~* 'eslam'
GROUP BY author
ORDER BY recordings DESC
LIMIT 10;

/*
 *                 author                 | recordings
 * ---------------------------------------+------------
 *  Rojo Córdova                          |         12
 *  Luis Ro                               |          8
 *  Caco Pontes                           |          6
 *  Jonatan Barreda Hernández Huachimingo |          5
 *  Josuelfo                              |          4
 *  Renato                                |          4
 *  Kevin Mara Kev                        |          4
 *  Hugo Cóatl                            |          4
 *  Maiiky Trauma                         |          4
 *  Victoria Tyler                        |          4
 *
 */