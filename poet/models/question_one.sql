-- OLD version of 'Total number of recordings.' Outputs 197
SELECT
  count(*)
FROM pista_son ps
JOIN serie s2 ON ps.serie_id = s2.serie_id
WHERE s2.nom_serie ~* 'eslam';

-- NEW version of 'Total number of recordings.' Outputs 197
SELECT
  count(*)
FROM poet_work s
JOIN poet_work_to_work_rel rel ON s.id = rel.from_model_id
JOIN poet_work p ON rel.to_model_id = p.id
WHERE s.work_type = 'SERIES'
AND p.work_type = 'PISTA SON'
AND s.full_name ~* 'eslam';

-- OLD version of 'Total number of compositions.' Outputs 193
SELECT
  count(DISTINCT c2.composicion_id)
FROM pista_son ps
JOIN serie s2 ON ps.serie_id = s2.serie_id
JOIN composicion c2 ON ps.composicion_id = c2.composicion_id
WHERE s2.nom_serie ~* 'eslam';

-- NEW version of 'Total number of compositions.' Outputs 193
SELECT
  count(*)
FROM poet_work s
JOIN poet_work_to_work_rel rel ON s.id = rel.from_model_id
JOIN poet_work p ON rel.to_model_id = p.id
WHERE s.work_type = 'SERIES'
AND p.work_type = 'COMPOSICION'
AND s.full_name ~* 'eslam';

