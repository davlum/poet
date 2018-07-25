# Generated by Django 2.0.6 on 2018-06-25 04:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('poet', '0000_refactor_db')
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'album',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Archivo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('etiqueta', models.TextField(blank=True, null=True)),
                ('nom', models.TextField()),
                ('pista_son_id', models.IntegerField()),
                ('duracion', models.IntegerField()),
                ('abr', models.IntegerField()),
                ('canales', models.IntegerField()),
                ('codec', models.TextField(blank=True, null=True)),
                ('frecuencia', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'archivo',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Cobertura',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_comienzo', models.CharField(blank=True, max_length=10, null=True)),
                ('fecha_finale', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'db_table': 'cobertura',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='CoberturaLicencia',
            fields=[
                ('cobertura_lic_id', models.AutoField(primary_key=True, serialize=False)),
                ('licencia_cobertura', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'cobertura_licencia',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='CoberturaTipo',
            fields=[
                ('tipo_cob', models.TextField(primary_key=True, serialize=False)),
                ('coment_cob', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'cobertura_tipo',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Composicion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.TextField()),
                ('nom_alt', models.TextField(blank=True, null=True)),
                ('fecha_pub', models.CharField(blank=True, max_length=10, null=True)),
                ('texto', models.TextField(blank=True, null=True)),
                ('estado', models.TextField()),
            ],
            options={
                'db_table': 'composicion',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='FamiliaInstrumento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.TextField(unique=True)),
            ],
            options={
                'db_table': 'familia_instrumento',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='GeneroMusical',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.TextField(unique=True)),
                ('coment', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'genero_musical',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='GeneroPersona',
            fields=[
                ('nom_genero', models.TextField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'genero_persona',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='GeneroPista',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gen_mus', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='poet.GeneroMusical')),
            ],
            options={
                'db_table': 'genero_pista',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Idioma',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.TextField(unique=True)),
            ],
            options={
                'db_table': 'idioma',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='IdiomaComposicion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('composicion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poet.Composicion')),
                ('idioma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poet.Idioma')),
            ],
            options={
                'db_table': 'idioma_composicion',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Instrumento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.TextField()),
                ('electronico', models.NullBooleanField()),
                ('instrumento_comentario', models.TextField(blank=True, null=True)),
                ('familia_instr', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='poet.FamiliaInstrumento')),
            ],
            options={
                'db_table': 'instrumento',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Lugar',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ciudad', models.TextField(blank=True, null=True)),
                ('subdivision', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'lugar',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Medio',
            fields=[
                ('nom_medio', models.TextField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'medio',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('nom_pais', models.TextField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'pais',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Participante',
            fields=[
                ('part_id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'participante',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ParticipanteCobertura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cobertura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poet.Cobertura')),
            ],
            options={
                'db_table': 'participante_cobertura',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ParticipanteComposicion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datos_personalizados', models.TextField(blank=True, null=True)),
                ('estado', models.TextField()),
            ],
            options={
                'db_table': 'participante_composicion',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ParticipantePistaSon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datos_personalizados', models.TextField(blank=True, null=True)),
                ('estado', models.TextField()),
            ],
            options={
                'db_table': 'participante_pista_son',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Permiso',
            fields=[
                ('nom_permiso', models.TextField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'permiso',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PersonaGrupo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_comienzo', models.CharField(blank=True, max_length=10, null=True)),
                ('fecha_finale', models.CharField(blank=True, max_length=10, null=True)),
                ('titulo', models.TextField(blank=True, null=True)),
                ('estado', models.TextField()),
            ],
            options={
                'db_table': 'persona_grupo',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PistaSon',
            fields=[
                ('pista_son_id', models.AutoField(primary_key=True, serialize=False)),
                ('numero_de_pista', models.IntegerField(blank=True, null=True)),
                ('coment_pista_son', models.TextField(blank=True, null=True)),
                ('fecha_grab', models.CharField(blank=True, max_length=10, null=True)),
                ('fecha_dig', models.CharField(blank=True, max_length=10, null=True)),
                ('fecha_cont', models.CharField(blank=True, max_length=10, null=True)),
                ('estado', models.TextField()),
                ('composicion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='poet.Composicion')),
                ('generos', models.ManyToManyField(through='poet.GeneroPista', to='poet.GeneroMusical')),
                ('lugar', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='poet.Lugar')),
                ('medio', models.ForeignKey(blank=True, db_column='medio', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='poet.Medio')),
            ],
            options={
                'db_table': 'pista_son',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='RolComposicion',
            fields=[
                ('nom_rol_comp', models.TextField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'rol_composicion',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='RolPistaSon',
            fields=[
                ('nom_rol_pista', models.TextField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'rol_pista_son',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Serie',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.TextField()),
                ('giro', models.TextField(blank=True, null=True)),
                ('ruta_foto', models.TextField(blank=True, null=True)),
                ('coment', models.TextField(blank=True, null=True)),
                ('estado', models.TextField()),
            ],
            options={
                'db_table': 'serie',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Tema',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.TextField(unique=True)),
            ],
            options={
                'db_table': 'tema',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TemaComposicion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('composicion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poet.Composicion')),
                ('tema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poet.Tema')),
            ],
            options={
                'db_table': 'tema_composicion',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TipoGrupo',
            fields=[
                ('nom_tipo_grupo', models.TextField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'tipo_grupo',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('part', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='poet.Participante')),
                ('email', models.TextField(blank=True, null=True, unique=True)),
                ('nom_part', models.TextField(blank=True, null=True)),
                ('sitio_web', models.TextField(blank=True, null=True)),
                ('direccion', models.TextField(blank=True, null=True)),
                ('telefono', models.TextField(blank=True, null=True)),
                ('fecha_comienzo', models.CharField(blank=True, max_length=10, null=True)),
                ('fecha_finale', models.CharField(blank=True, max_length=10, null=True)),
                ('coment_part', models.TextField(blank=True, null=True)),
                ('estado', models.TextField()),
            ],
            options={
                'db_table': 'grupo',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('part', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='poet.Participante')),
                ('nom_paterno', models.TextField(blank=True, null=True)),
                ('nom_materno', models.TextField(blank=True, null=True)),
                ('seudonimo', models.TextField(blank=True, null=True)),
                ('ruta_foto', models.TextField(blank=True, null=True)),
                ('email', models.TextField(blank=True, null=True, unique=True)),
                ('nom_part', models.TextField(blank=True, null=True)),
                ('sitio_web', models.TextField(blank=True, null=True)),
                ('direccion', models.TextField(blank=True, null=True)),
                ('telefono', models.TextField(blank=True, null=True)),
                ('fecha_comienzo', models.CharField(blank=True, max_length=10, null=True)),
                ('fecha_finale', models.CharField(blank=True, max_length=10, null=True)),
                ('coment_part', models.TextField(blank=True, null=True)),
                ('estado', models.TextField()),
            ],
            options={
                'db_table': 'persona',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='poet.Participante')),
                ('confirmado', models.BooleanField()),
                ('nom_usuario', models.TextField(unique=True)),
                ('contrasena', models.TextField()),
                ('fecha_registro', models.DateTimeField(blank=True, null=True)),
                ('fecha_confirmado', models.DateTimeField(blank=True, null=True)),
                ('prohibido', models.BooleanField()),
                ('gr_email', models.OneToOneField(blank=True, db_column='gr_email', null=True, on_delete=django.db.models.deletion.PROTECT, to='poet.Grupo')),
                ('permiso', models.ForeignKey(db_column='permiso', on_delete=django.db.models.deletion.DO_NOTHING, to='poet.Permiso')),
                ('pers_email', models.OneToOneField(blank=True, db_column='pers_email', null=True, on_delete=django.db.models.deletion.PROTECT, to='poet.Persona')),
            ],
            options={
                'db_table': 'usuario',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='serie',
            name='cargador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='poet.Participante'),
        ),
        migrations.AddField(
            model_name='pistason',
            name='participantes',
            field=models.ManyToManyField(through='poet.ParticipantePistaSon', to='poet.Participante'),
        ),
        migrations.AddField(
            model_name='pistason',
            name='serie',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='poet.Serie'),
        ),
        migrations.AddField(
            model_name='personagrupo',
            name='cargador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='poet.Participante'),
        ),
        migrations.AddField(
            model_name='participantepistason',
            name='cargador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='part_pista_uploader', to='poet.Participante'),
        ),
        migrations.AddField(
            model_name='participantepistason',
            name='instrumento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='poet.Instrumento'),
        ),
        migrations.AddField(
            model_name='participantepistason',
            name='part',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poet.Participante'),
        ),
        migrations.AddField(
            model_name='participantepistason',
            name='pista_son',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poet.PistaSon'),
        ),
        migrations.AddField(
            model_name='participantepistason',
            name='rol_pista_son',
            field=models.ForeignKey(db_column='rol_pista_son', on_delete=django.db.models.deletion.DO_NOTHING, to='poet.RolPistaSon'),
        ),
        migrations.AddField(
            model_name='participantecomposicion',
            name='cargador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='part_comp_uploader', to='poet.Participante'),
        ),
        migrations.AddField(
            model_name='participantecomposicion',
            name='composicion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poet.Composicion'),
        ),
        migrations.AddField(
            model_name='participantecomposicion',
            name='part',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poet.Participante'),
        ),
        migrations.AddField(
            model_name='participantecomposicion',
            name='rol_composicion',
            field=models.ForeignKey(db_column='rol_composicion', on_delete=django.db.models.deletion.DO_NOTHING, to='poet.RolComposicion'),
        ),
        migrations.AddField(
            model_name='participantecobertura',
            name='part',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poet.Participante'),
        ),
        migrations.AddField(
            model_name='participante',
            name='coberturas',
            field=models.ManyToManyField(through='poet.ParticipanteCobertura', to='poet.Cobertura'),
        ),
        migrations.AddField(
            model_name='lugar',
            name='pais',
            field=models.ForeignKey(blank=True, db_column='pais', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='poet.Pais'),
        ),
        migrations.AddField(
            model_name='generopista',
            name='pista_son',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='poet.PistaSon'),
        ),
        migrations.AddField(
            model_name='composicion',
            name='cargador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='composicion_uploader', to='poet.Participante'),
        ),
        migrations.AddField(
            model_name='composicion',
            name='composicion_orig',
            field=models.ForeignKey(blank=True, db_column='composicion_orig', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='poet.Composicion'),
        ),
        migrations.AddField(
            model_name='composicion',
            name='idiomas',
            field=models.ManyToManyField(through='poet.IdiomaComposicion', to='poet.Idioma'),
        ),
        migrations.AddField(
            model_name='composicion',
            name='participantes',
            field=models.ManyToManyField(through='poet.ParticipanteComposicion', to='poet.Participante'),
        ),
        migrations.AddField(
            model_name='composicion',
            name='temas',
            field=models.ManyToManyField(through='poet.TemaComposicion', to='poet.Tema'),
        ),
        migrations.AddField(
            model_name='coberturalicencia',
            name='tipo_cob',
            field=models.ForeignKey(blank=True, db_column='tipo_cob', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='poet.CoberturaTipo'),
        ),
        migrations.AddField(
            model_name='cobertura',
            name='cobertura_lic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='poet.CoberturaLicencia'),
        ),
        migrations.AddField(
            model_name='cobertura',
            name='composicion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='poet.Composicion'),
        ),
        migrations.AddField(
            model_name='cobertura',
            name='pais_cobertura',
            field=models.ForeignKey(blank=True, db_column='pais_cobertura', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='poet.Pais'),
        ),
        migrations.AddField(
            model_name='cobertura',
            name='pista_son',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='poet.PistaSon'),
        ),
        migrations.AddField(
            model_name='album',
            name='serie',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='poet.Serie'),
        ),
        migrations.AlterUniqueTogether(
            name='temacomposicion',
            unique_together={('composicion', 'tema')},
        ),
        migrations.AddField(
            model_name='serie',
            name='mod',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='poet.Usuario'),
        ),
        migrations.AddField(
            model_name='pistason',
            name='cargador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='pista_uploader', to='poet.Usuario'),
        ),
        migrations.AddField(
            model_name='pistason',
            name='mod',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='poet.Usuario'),
        ),
        migrations.AddField(
            model_name='personagrupo',
            name='grupo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poet.Grupo'),
        ),
        migrations.AddField(
            model_name='personagrupo',
            name='mod',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='poet.Usuario'),
        ),
        migrations.AddField(
            model_name='personagrupo',
            name='persona',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poet.Persona'),
        ),
        migrations.AddField(
            model_name='persona',
            name='cargador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='persona_uploader', to='poet.Participante'),
        ),
        migrations.AddField(
            model_name='persona',
            name='genero',
            field=models.ForeignKey(blank=True, db_column='genero', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='poet.GeneroPersona'),
        ),
        migrations.AddField(
            model_name='persona',
            name='lugar',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='poet.Lugar'),
        ),
        migrations.AddField(
            model_name='persona',
            name='lugar_muer',
            field=models.ForeignKey(blank=True, db_column='lugar_muer', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='place_of_death', to='poet.Lugar'),
        ),
        migrations.AddField(
            model_name='persona',
            name='mod',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='poet.Usuario'),
        ),
        migrations.AddField(
            model_name='participantepistason',
            name='mod',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='poet.Usuario'),
        ),
        migrations.AddField(
            model_name='participantecomposicion',
            name='mod',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='poet.Usuario'),
        ),
        migrations.AlterUniqueTogether(
            name='participantecobertura',
            unique_together={('cobertura', 'part')},
        ),
        migrations.AlterUniqueTogether(
            name='idiomacomposicion',
            unique_together={('composicion', 'idioma')},
        ),
        migrations.AddField(
            model_name='grupo',
            name='cargador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='grupo_uploader', to='poet.Participante'),
        ),
        migrations.AddField(
            model_name='grupo',
            name='lugar',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='poet.Lugar'),
        ),
        migrations.AddField(
            model_name='grupo',
            name='mod',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='poet.Usuario'),
        ),
        migrations.AddField(
            model_name='grupo',
            name='personas',
            field=models.ManyToManyField(through='poet.PersonaGrupo', to='poet.Persona'),
        ),
        migrations.AddField(
            model_name='grupo',
            name='tipo_grupo',
            field=models.ForeignKey(blank=True, db_column='tipo_grupo', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='poet.TipoGrupo'),
        ),
        migrations.AlterUniqueTogether(
            name='generopista',
            unique_together={('pista_son', 'gen_mus')},
        ),
        migrations.AddField(
            model_name='composicion',
            name='mod',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='mod', to='poet.Usuario'),
        ),
        migrations.AlterUniqueTogether(
            name='personagrupo',
            unique_together={('persona', 'grupo')},
        ),
        migrations.AlterUniqueTogether(
            name='participantepistason',
            unique_together={('pista_son', 'part', 'rol_pista_son', 'instrumento')},
        ),
        migrations.AlterUniqueTogether(
            name='participantecomposicion',
            unique_together={('composicion', 'part', 'rol_composicion')},
        ),
    ]
