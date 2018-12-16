-- OLD version of 'Total number of composers.' Outputs 128
SELECT
  count(DISTINCT pc.part_id)
FROM pista_son ps
JOIN serie s2 ON ps.serie_id = s2.serie_id
JOIN composicion c2 ON ps.composicion_id = c2.composicion_id
JOIN participante_composicion pc ON c2.composicion_id = pc.composicion_id
WHERE s2.nom_serie ~* 'eslam'
AND pc.rol_composicion = 'Composición';

-- NEW version of 'Total number of composers.' Outputs 128
SELECT
  count(DISTINCT e_to_c.from_model_id)
FROM poet_work c
JOIN poet_work_to_work_rel s_to_c ON c.id = s_to_c.to_model_id
JOIN poet_work s ON s_to_c.from_model_id = s.id
JOIN poet_entity_to_work_rel e_to_c on c.id = e_to_c.to_model_id
WHERE s.full_name ~* 'eslam'
AND c.work_type = 'COMPOSICION'
AND s.work_type = 'SERIES'
AND e_to_c.role = 'Composición';

-- OLD version of 'Total number of performers.' Outputs 123
SELECT
  count(DISTINCT s3.part_id)
FROM pista_son ps
JOIN serie s2 ON ps.serie_id = s2.serie_id
JOIN participante_pista_son s3 on ps.pista_son_id = s3.pista_son_id
WHERE s2.nom_serie ~* 'eslam'
AND s3.rol_pista_son IN ('Lectura en voz alta', 'Interpretación musical');

-- NEW version of 'Total number of performers.' Outputs 123
SELECT
  count(DISTINCT e_to_t.from_model_id)
FROM poet_work t
JOIN poet_work_to_work_rel s_to_t ON t.id = s_to_t.to_model_id
JOIN poet_work s ON s_to_t.from_model_id = s.id
JOIN poet_entity_to_work_rel e_to_t on t.id = e_to_t.to_model_id
WHERE s.full_name ~* 'eslam'
AND T.work_type = 'PISTA SON'
AND s.work_type = 'SERIES'
AND e_to_t.role IN ('Lectura en voz alta', 'Interpretación musical');

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

-- NEW version of 'Total number of composers and interpreters.' Outputs 131
SELECT
  count(DISTINCT e_to_s.from_model_id)
FROM poet_work s
JOIN poet_entity_to_work_rel e_to_s on s.id = e_to_s.to_model_id
WHERE s.full_name ~* 'eslam'
AND s.work_type = 'SERIES'
AND e_to_s.role IN ('Lectura en voz alta', 'Interpretación musical', 'Composición');

