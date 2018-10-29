-- OLD version of 'Total number of recordings.' Outputs 197
SELECT
  count(*)
FROM pista_son ps
JOIN serie s2 ON ps.serie_id = s2.serie_id;

-- OLD version of 'Total number of compositions.' Outputs 193
SELECT
  count(DISTINCT c2.composicion_id)
FROM pista_son ps
JOIN serie s2 ON ps.serie_id = s2.serie_id
JOIN composicion c2 ON ps.composicion_id = c2.composicion_id;

-- OLD version of 'Total number of composers.' Outputs 128
SELECT
  count(DISTINCT pc.part_id)
FROM pista_son ps
JOIN serie s2 ON ps.serie_id = s2.serie_id
JOIN composicion c2 ON ps.composicion_id = c2.composicion_id
JOIN participante_composicion pc ON c2.composicion_id = pc.composicion_id
WHERE s2.nom_serie ~* 'eslam'
AND pc.rol_composicion = 'Composición';

-- OLD version of 'Total number of performers.' Outputs 123
SELECT
  count(DISTINCT s3.part_id)
FROM pista_son ps
JOIN serie s2 ON ps.serie_id = s2.serie_id
JOIN participante_pista_son s3 on ps.pista_son_id = s3.pista_son_id
WHERE s2.nom_serie ~* 'eslam'
AND s3.rol_pista_son IN ('Lectura en voz alta', 'Interpretación musical');

-- OLD version of 'Total number of composers and interpreters.' Outputs 131
SELECT count(DISTINCT u.part_id) FROM ((
  SELECT pc.part_id
  FROM pista_son ps
  JOIN serie s2 ON ps.serie_id = s2.serie_id
  JOIN composicion c2 ON ps.composicion_id = c2.composicion_id
  JOIN participante_composicion pc ON c2.composicion_id = pc.composicion_id
  WHERE s2.nom_serie ~* 'eslam'
  AND pc.rol_composicion = 'Composición'
  ) UNION (
  SELECT DISTINCT s3.part_id
  FROM pista_son ps
  JOIN serie s2 ON ps.serie_id = s2.serie_id
  JOIN participante_pista_son s3 on ps.pista_son_id = s3.pista_son_id
  WHERE s2.nom_serie ~* 'eslam'
  AND s3.rol_pista_son IN ('Lectura en voz alta', 'Interpretación musical')
  )) u;

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

-- OLD Top 5 interpreters with more recordings (i.e., interpretations) and total recordings per interpreter.
SELECT
   array_to_string(array_remove(ARRAY[
     p.nom_part,
     g.nom_part,
     p.seudonimo,
     p.nom_materno,
     p.nom_paterno], ' '), '') author,
  count(son.pista_son_id) recordings
FROM participante_pista_son son
LEFT JOIN persona p ON p.part_id = son.part_id
LEFT JOIN grupo g ON g.part_id = son.part_id
JOIN pista_son ps ON ps.pista_son_id = son.pista_son_id
JOIN serie s ON s.id = ps.serie_id
WHERE son.rol_pista_son IN ('Lectura en voz alta', 'Interpretación musical')
AND s.nom ~* 'eslam'
GROUP BY author
ORDER BY recordings DESC;

/*
 *                 author               | recordings
 *  ------------------------------------+------------
 *   RojoCórdova                        |         12
 *   LuisRo                             |         12
 *   CacoPontes                         |         10
 *   Maiiky Trauma                      |          8
 *   VictoriaTyler
           |          7
 *   Josuelfo                           |          5
 *   JonatanHuachimingoBarredaHernández |          5
 *   Hugo Cóatl                         |          4
 *   Renato                             |          4
 *   KevinKevMara                       |          4
 *   AndreaAndah Irie                   |          4
 *   ÉdgarTorres                        |          3
 *   AlfredoSantiago                    |          3
 *   Furor Sanandi                      |          3
 *   DiegoPingüinoMedina                |          3
 *   MarleneKashianKemmerSagredo        |          3
 *   IvánVan-TSalgueroTorres            |          3
 *   PaulaKlein                         |          3
 *   Pito Amor                          |          3
 *   América                            |          3
 *   Susanita                           |          3
 *   KarlaPáez                          |          3
 *   AndrésIxca CienfuegosGalindo       |          3
 *   Fernando                           |          2
 *   Rashid                             |          2
 *   CarlosKarloz AtlRamírez            |          2
 *   Homodon                            |          2
 *   CarlosPineda                       |          2
 *   HebeRosell                         |          2
 *   El Violín                          |          2
 *   CarlosTitosBarraza                 |          2
 *   Betsy Numen                        |          2
 *   Lucía                              |          2
 *   Basher                             |          2
 *   Spring Ramírez                     |          2
 *   CinthiaCandelas                    |          2
 *   AdolfoLópezGuzmán                  |          2
 *   Alejandro                          |          2
 *   UlisesSad CLópez                   |          2
 *   Bronte                             |          2
 *   EdmeéDiosa LocaGarcía              |          2
 *   Juan Pablo                         |          2
 *   Jahir                              |          2
 *   Nómada                             |          2
 *   DonNet                             |          2
 *   MC L-On                            |          2
 *   Kilamastra                         |          1
 *   LoganPhillips                      |          1
 *   MC Ewor                            |          1
 *   Majo                               |          1
 *
 */