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
 *   VictoriaTyler                      |          7
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