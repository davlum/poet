# Must run before initial migration

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.RunSQL("""
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
      """),
        migrations.RunSQL("""
CREATE OR REPLACE FUNCTION fix_date(target_table REGCLASS, target_col text) RETURNS void AS $body$
BEGIN
  EXECUTE format('ALTER TABLE %I ' ||
                 'ALTER COLUMN %I TYPE VARCHAR USING get_fecha(%I) ', target_table, target_col, target_col);
END;
$body$
LANGUAGE plpgsql;
       
       """),

        # Drop views
        migrations.RunSQL('DROP VIEW gr_view CASCADE;'),
        migrations.RunSQL('DROP VIEW part_view CASCADE;'),
        migrations.RunSQL('DROP VIEW pers_view CASCADE;'),

        # Drop schema audit and associated functions
        migrations.RunSQL('DROP SCHEMA IF EXISTS audit CASCADE;'),

        migrations.RunSQL('DROP FUNCTION IF EXISTS public.audit_populated_table(regclass, integer, text) CASCADE;'),
        migrations.RunSQL('DROP FUNCTION IF EXISTS public.audit_table(regclass) CASCADE;'),
        migrations.RunSQL('DROP FUNCTION IF EXISTS public.gen_table(regclass) CASCADE;'),
        migrations.RunSQL('DROP FUNCTION IF EXISTS public.gr_insert() CASCADE;'),
        migrations.RunSQL('DROP FUNCTION IF EXISTS public.nom(text, text, text, text) CASCADE;'),
        migrations.RunSQL('DROP FUNCTION IF EXISTS public.participante_insert() CASCADE;'),
        migrations.RunSQL('DROP FUNCTION IF EXISTS public.pers_insert() CASCADE;'),
        migrations.RunSQL('DROP FUNCTION IF EXISTS public.process_audit() CASCADE;'),
        migrations.RunSQL('DROP FUNCTION IF EXISTS public.set_fecha(fecha) CASCADE;'),
        migrations.RunSQL('DROP FUNCTION IF EXISTS public.strip(text) CASCADE;'),
        migrations.RunSQL('DROP FUNCTION IF EXISTS public.us_grupo_insert() CASCADE;'),
        migrations.RunSQL('DROP FUNCTION IF EXISTS public.us_pers_insert() CASCADE;'),
        migrations.RunSQL('DROP FUNCTION IF EXISTS public.usuario_id_insert() CASCADE;'),

        # Change date type to string
        migrations.RunSQL("SELECT fix_date('cobertura', 'fecha_comienzo');"),
        migrations.RunSQL("SELECT fix_date('cobertura', 'fecha_finale');"),
        migrations.RunSQL("SELECT fix_date('composicion', 'fecha_pub');"),
        migrations.RunSQL("SELECT fix_date('grupo', 'fecha_comienzo');"),
        migrations.RunSQL("SELECT fix_date('grupo', 'fecha_finale');"),
        migrations.RunSQL("SELECT fix_date('persona', 'fecha_comienzo'); "),
        migrations.RunSQL("SELECT fix_date('persona', 'fecha_finale');"),
        migrations.RunSQL("SELECT fix_date('persona_grupo', 'fecha_comienzo');"),
        migrations.RunSQL("SELECT fix_date('persona_grupo', 'fecha_finale');"),
        migrations.RunSQL("SELECT fix_date('pista_son', 'fecha_cont');"),
        migrations.RunSQL("SELECT fix_date('pista_son', 'fecha_dig');"),
        migrations.RunSQL("SELECT fix_date('pista_son', 'fecha_grab');"),

        # Rename columns
        migrations.RunSQL("ALTER TABLE idioma RENAME COLUMN idioma_id TO id"),
        migrations.RunSQL("ALTER TABLE idioma RENAME COLUMN nom_idioma TO nom"),

        migrations.RunSQL("ALTER TABLE tema RENAME COLUMN tema_id TO id"),
        migrations.RunSQL("ALTER TABLE tema RENAME COLUMN nom_tema TO nom"),

        migrations.RunSQL("ALTER TABLE genero_musical RENAME COLUMN gen_mus_id TO id"),
        migrations.RunSQL("ALTER TABLE genero_musical RENAME COLUMN nom_gen_mus TO nom"),
        migrations.RunSQL("ALTER TABLE genero_musical RENAME COLUMN coment_gen_mus TO coment"),

        migrations.RunSQL("ALTER TABLE album RENAME COLUMN album_id TO id"),
        migrations.RunSQL("ALTER TABLE album RENAME COLUMN nom_album TO nom"),

        migrations.RunSQL("ALTER TABLE serie RENAME COLUMN serie_id TO id"),
        migrations.RunSQL("ALTER TABLE serie RENAME COLUMN nom_serie TO nom"),
        migrations.RunSQL("ALTER TABLE serie RENAME COLUMN coment_serie TO coment"),

        migrations.RunSQL("ALTER TABLE familia_instrumento RENAME COLUMN familia_instr_id TO id"),
        migrations.RunSQL("ALTER TABLE familia_instrumento RENAME COLUMN nom_familia_instr TO nom"),

        migrations.RunSQL("ALTER TABLE instrumento RENAME COLUMN instrumento_id TO id"),
        migrations.RunSQL("ALTER TABLE instrumento RENAME COLUMN nom_inst TO nom"),
        migrations.RunSQL("ALTER TABLE instrumento RENAME COLUMN instrumento_comentario TO coment"),

        migrations.RunSQL("ALTER TABLE archivo RENAME COLUMN archivo_id TO id"),

        migrations.RunSQL("ALTER TABLE cobertura RENAME COLUMN cobertura_id TO id"),
        migrations.RunSQL("ALTER TABLE cobertura_licencia RENAME COLUMN cobertura_lic_id TO id"),

        migrations.RunSQL("ALTER TABLE composicion RENAME COLUMN composicion_id TO id"),
        migrations.RunSQL("ALTER TABLE lugar RENAME COLUMN lugar_id TO id"),

        # Drop unnecessary tables
        # migrations.RunSQL("DROP TABLE medio")
    ]
