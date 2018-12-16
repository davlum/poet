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


DROP VIEW IF EXISTS gr_view CASCADE;
DROP VIEW IF EXISTS part_view CASCADE;
DROP VIEW IF EXISTS pers_view CASCADE;

-- Drop schema audit and associated functions
DROP SCHEMA IF EXISTS audit CASCADE;

DROP FUNCTION IF EXISTS public.audit_populated_table(regclass, integer, text) CASCADE;
DROP FUNCTION IF EXISTS public.audit_table(regclass) CASCADE;
DROP FUNCTION IF EXISTS public.gen_table(regclass) CASCADE;
DROP FUNCTION IF EXISTS public.gr_insert() CASCADE;
DROP FUNCTION IF EXISTS public.nom(text, text, text, text) CASCADE;
DROP FUNCTION IF EXISTS public.participante_insert() CASCADE;
DROP FUNCTION IF EXISTS public.pers_insert() CASCADE;
DROP FUNCTION IF EXISTS public.process_audit() CASCADE;
DROP FUNCTION IF EXISTS public.set_fecha(fecha) CASCADE;
DROP FUNCTION IF EXISTS public.strip(text) CASCADE;
DROP FUNCTION IF EXISTS public.us_grupo_insert() CASCADE;
DROP FUNCTION IF EXISTS public.us_pers_insert() CASCADE;
DROP FUNCTION IF EXISTS public.usuario_id_insert() CASCADE;

SELECT fix_date('cobertura', 'fecha_comienzo');
SELECT fix_date('cobertura', 'fecha_finale');
SELECT fix_date('composicion', 'fecha_pub');
SELECT fix_date('grupo', 'fecha_comienzo');
SELECT fix_date('grupo', 'fecha_finale');
SELECT fix_date('persona', 'fecha_comienzo');
SELECT fix_date('persona', 'fecha_finale');
SELECT fix_date('persona_grupo', 'fecha_comienzo');
SELECT fix_date('persona_grupo', 'fecha_finale');
SELECT fix_date('pista_son', 'fecha_cont');
SELECT fix_date('pista_son', 'fecha_dig');
SELECT fix_date('pista_son', 'fecha_grab');