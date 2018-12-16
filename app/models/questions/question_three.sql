-- OLD Interpreters using instruments other than voice or reading out loud, ordered by title, series, and name of instrument used.
SELECT
   array_to_string(array_remove(ARRAY[c.nom, c.nom_alt], ''), ' ') composition,
   array_to_string(array_remove(ARRAY[
     p.nom_part,
     g.nom_part,
     p.seudonimo,
     p.nom_materno,
     p.nom_paterno], ''), ' ') author,
   s.nom series,
   i.nom instrument
FROM participante_pista_son pc
JOIN pista_son ps ON pc.pista_son_id = ps.pista_son_id
JOIN composicion c ON c.id = ps.composicion_id
JOIN serie s ON s.id = ps.serie_id
JOIN instrumento i ON i.id = pc.instrumento_id
LEFT JOIN persona p ON pc.part_id = p.part_id
LEFT JOIN grupo g ON pc.part_id = g.part_id
WHERE i.nom <> 'Voz'
AND i.nom <> 'Ninguno'
AND s.nom ~* 'eslam'
ORDER BY
  composition,
  series,
  instrument;

SELECT
   array_to_string(array_remove(ARRAY[c.nom, c.nom_alt], ' '), '') composition,
   array_to_string(array_remove(ARRAY[
     p.nom_part,
     g.nom_part,
     p.seudonimo,
     p.nom_materno,
     p.nom_paterno], ''), ' ') author,
   s.nom series,
   i.nom instrument
FROM participante_pista_son pc
JOIN pista_son ps ON pc.pista_son_id = ps.pista_son_id
JOIN composicion c ON c.id = ps.composicion_id
JOIN serie s ON s.id = ps.serie_id
JOIN instrumento i ON i.id = pc.instrumento_id
LEFT JOIN persona p ON pc.part_id = p.part_id
LEFT JOIN grupo g ON pc.part_id = g.part_id
-- WHERE i.nom <> 'Voz'
-- AND i.nom <> 'Ninguno'
WHERE s.nom ~* 'eslam'
AND c.nom ~ 'levanta';

/*
 *
 *                  composition                |         author          |                       series                        |       instrument
 *  ------------------------------------------+-------------------------+-----------------------------------------------------+-------------------------
 *   "Aire enrarecido..."                     | AndreaAndah Irie        | Eslam de poesía 31 Rojo Córdova CCD                 | Guitarra acústica
 *   "Hoy soñé que me casé contigo..."        | Josuelfo                | Eslam de poesía 29 Rojo Córdova CCD                 | Palmas
 *   "Soy la aurora forjada en el universo.." | Basher                  | Eslam de poesía 27 Rojo Córdova CCD                 | Palmas
 *   01011001                                 | The Knife               | eSLAMex: Primera antología de espoken word mexicano | Sintetizador digital
 *   Coração                                  | CacoPontes              | Eslam de poesía 33 Rojo Córdova CCD                 | Percusiones
 *   Fiesta de disfraces                      | AndreaAndah Irie        | Eslam de poesía 31 Rojo Córdova CCD                 | Guitarra acústica
 *   Hip-Hop                                  | IvánVan-TSalgueroTorres | eSLAMex: Primera antología de espoken word mexicano | Programa de computadora
 *   Hip-Hop                                  | IvánVan-TSalgueroTorres | eSLAMex: Primera antología de espoken word mexicano | Tornamesa
 *   Iemanjá Janaína                          | CacoPontes              | Eslam de poesía 33 Rojo Córdova CCD                 | Percusiones
 *   Inefable                                 | Josuelfo                | Eslam de poesía 27 Rojo Córdova CCD                 | Palmas
 *   Línea B                                  | Homodon                 | eSLAMex: Primera antología de espoken word mexicano | Tornamesa
 *   Melô do Pen Drive                        | CacoPontes              | Eslam de poesía 33 Rojo Córdova CCD                 | Percusiones
 *   Pantalones anchos                        | MC L-On                 | eSLAMex: Primera antología de espoken word mexicano | Programa de computadora
 *   Radiotransmisor                          | ÉdgarTorres             | eSLAMex: Primera antología de espoken word mexicano | Bajo eléctrico
 *   Radiotransmisor                          | ÉdgarTorres             | eSLAMex: Primera antología de espoken word mexicano | Caja de ritmos
 *   Radiotransmisor                          | ÉdgarTorres             | eSLAMex: Primera antología de espoken word mexicano | Guitarra eléctrica
 *   Samba mal-educado                        | CacoPontes              | Eslam de poesía 33 Rojo Córdova CCD                 | Percusiones
 *
 */

-- NEW Interpreters using instruments other than voice or reading out loud, ordered by title, series, and name of instrument used.
SELECT DISTINCT
  array_to_string(array_remove(ARRAY[c.full_name, c.alt_name], ''), ' ') composition,
  array_to_string(array_remove(ARRAY[e.full_name, e.alt_name], ''), ' ') author,
  s.full_name series,
  e_to_s.role,
  e_to_s.additional_data->>'instrument' instrument
FROM poet_work s
JOIN poet_work_to_work_rel s_to_c ON s.id = s_to_c.from_model_id
JOIN poet_work c ON c.id = s_to_c.to_model_id
JOIN poet_entity_to_work_rel e_to_s ON s.id = e_to_s.to_model_id
JOIN poet_entity e ON e.id = e_to_s.from_model_id
WHERE s.full_name ~* 'eslam'
AND s.work_type = 'SERIES'
AND c.work_type = 'COMPOSICION'
AND e_to_s.additional_data ? 'instrument'
AND e_to_s.additional_data->>'instrument' <> 'Voz'
AND e_to_s.additional_data->>'instrument' <> 'Ninguno'
ORDER BY
  composition,
  series,
  instrument;


SELECT DISTINCT
  array_to_string(array_remove(ARRAY[c.full_name, c.alt_name], ' '), '') composition,
  array_to_string(array_remove(ARRAY[e.full_name, e.alt_name], ' '), '') author,
  s.full_name series,
  e_to_s.role
--   e_to_s.additional_data->>'instrument' instrument
FROM poet_work s
JOIN poet_work_to_work_rel s_to_c ON s.id = s_to_c.from_model_id
JOIN poet_work c ON c.id = s_to_c.to_model_id
JOIN poet_entity_to_work_rel e_to_s ON s.id = e_to_s.to_model_id
JOIN poet_entity e ON e.id = e_to_s.from_model_id
WHERE s.full_name ~* 'eslam'
AND s.work_type = 'SERIES'
AND c.work_type = 'COMPOSICION'
AND e_to_s.role = 'Interpretación musical'
AND c.full_name ~* 'levanta';
-- AND e_to_s.additional_data ? 'instrument'
-- AND e_to_s.additional_data->>'instrument' <> 'Voz'
-- AND e_to_s.additional_data->>'instrument' <> 'Ninguno'
-- ORDER BY
--   composition,
--   series,
--   instrument;