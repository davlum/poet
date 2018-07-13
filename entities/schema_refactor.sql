CREATE OR REPLACE FUNCTION drop_views() RETURNS VOID AS $body$
BEGIN
  SELECT 'DROP VIEW ' || table_name || ' CASCADE;'
    FROM information_schema.views
  WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
    AND table_name !~ '^pg_';
END;
$body$
LANGUAGE plpgsql
IMMUTABLE
RETURNS NULL ON NULL INPUT;

CREATE OR REPLACE FUNCTION get_fecha(fecha) RETURNS text AS $body$
BEGIN
    IF $1.t = 'YEAR' THEN
      RETURN to_char($1.d, 'YYYY');
    ELSIF $1.t = 'MONTH' THEN
      RETURN to_char($1.d, 'YYYY-MM');
    ELSE
      RETURN to_char($1.d, 'YYYY-MM-DD');
    END IF;
END;
$body$
LANGUAGE plpgsql
IMMUTABLE
RETURNS NULL ON NULL INPUT;


CREATE OR REPLACE FUNCTION fix_date(target_table REGCLASS, target_col text) RETURNS void AS $body$
BEGIN
  EXECUTE format('ALTER TABLE %I ' ||
                 'ALTER COLUMN %I TYPE VARCHAR USING get_fecha(%I) ', target_table, target_col, target_col);
END;
$body$
LANGUAGE plpgsql;

DROP SCHEMA IF EXISTS audit CASCADE;

/*

Table and column names can be fetched with this query.

SELECT
  quote_literal(table_name),
  quote_literal(column_name)
FROM information_schema.columns
WHERE column_name ~* 'fecha'
      AND data_type = 'USER-DEFINED';
*/

SELECT fix_date('cobertura'   , 'fecha_comienzo');
SELECT fix_date('cobertura'    ,'fecha_finale');
SELECT fix_date('composicion'  ,'fecha_pub');
SELECT fix_date('grupo'        ,'fecha_comienzo');
SELECT fix_date('grupo'        ,'fecha_finale');
SELECT fix_date('persona'      ,'fecha_comienzo');
SELECT fix_date('persona'      ,'fecha_finale');
SELECT fix_date('persona_grupo','fecha_comienzo');
SELECT fix_date('persona_grupo','fecha_finale');
SELECT fix_date('pista_son'    ,'fecha_cont');
SELECT fix_date('pista_son'    ,'fecha_dig');
SELECT fix_date('pista_son'    ,'fecha_grab');