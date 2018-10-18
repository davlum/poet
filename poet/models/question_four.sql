-- OLD Top 5 interpreters with more recordings (i.e., interpretations) and total recordings per interpreter.
SELECT
   array_to_string(array_remove(ARRAY[
     p.nom_part,
     g.nom_part,
     p.seudonimo,
     p.nom_materno,
     p.nom_paterno], ''), ' ') author,
  count(DISTINCT c.nom) recordings
FROM participante_pista_son son
LEFT JOIN persona p ON p.part_id = son.part_id
LEFT JOIN grupo g ON g.part_id = son.part_id
JOIN pista_son ps ON ps.pista_son_id = son.pista_son_id
JOIN composicion c ON c.id = ps.composicion_id
JOIN serie s ON s.id = ps.serie_id
WHERE son.rol_pista_son IN ('Lectura en voz alta', 'Interpretación musical')
AND s.nom ~* 'eslam'
GROUP BY author
ORDER BY recordings DESC;

/*
 *                  author                 | recordings
 *  ---------------------------------------+------------
 *   Rojo Córdova                          |         11
 *   Luis Ro                               |          8
 *   Caco Pontes                           |          6
 *   Jonatan Huachimingo Barreda Hernández |          5
 *   Hugo Cóatl                            |          4
 *
 */

        Column
-----------------------
 nom                 -- full name
 nom_alt             -- alt_name
 'Recording'         -- work_type
 numero_de_pista     -- ad
 medio               -- ad
 coment_pista_son    -- comment
 fecha_grab          -- ad
 fecha_dig           -- ad
 fecha_cont          -- ad
 city_of_origin      -- city
 country_of_origin   -- country
 fecha_pub
 composicion_orig    -- ad
 texto               -- Append to comments with concat(coment_pista_son, '\r', chr(10), '\r', chr(10), texto)
