# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils.translation import gettext as _


PUBLISHED = 'PUBLICADO'
DEPOSITED = 'DEPOSITAR'
REJECTED = 'REJECTED'
PENDING = 'PENDIENTE'
RELEASE_STATES_CHOICES = (
    (PUBLISHED, _('Published')),
    (DEPOSITED, _('Deposited')),
    (PENDING, _('Pending')),
    (REJECTED, _('Rejected')),
)


class Album(models.Model):
    id = models.AutoField(primary_key=True)
    serie = models.ForeignKey('Serie', models.DO_NOTHING, blank=True, null=True)
    nom = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'album'


class Archivo(models.Model):
    id = models.AutoField(primary_key=True)
    etiqueta = models.TextField(blank=True, null=True)
    nom = models.TextField()
    pista_son_id = models.IntegerField()
    duracion = models.IntegerField()
    abr = models.IntegerField()
    canales = models.IntegerField()
    codec = models.TextField(blank=True, null=True)
    frecuencia = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'archivo'


class Cobertura(models.Model):
    id = models.AutoField(primary_key=True)
    cobertura_lic = models.ForeignKey('CoberturaLicencia', models.DO_NOTHING)
    pista_son = models.ForeignKey('PistaSon', models.DO_NOTHING, blank=True, null=True)
    composicion = models.ForeignKey('Composicion', models.DO_NOTHING, blank=True, null=True)
    pais_cobertura = models.ForeignKey('Pais', models.DO_NOTHING, db_column='pais_cobertura', blank=True, null=True)
    fecha_comienzo = models.CharField(max_length=10, blank=True, null=True)
    fecha_finale = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'cobertura'


class CoberturaLicencia(models.Model):
    id = models.AutoField(primary_key=True)
    tipo_cob = models.ForeignKey('CoberturaTipo', models.DO_NOTHING, db_column='tipo_cob', blank=True, null=True)
    licencia_cobertura = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'cobertura_licencia'


class CoberturaTipo(models.Model):
    tipo_cob = models.TextField(primary_key=True)
    coment_cob = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'cobertura_tipo'


class Composicion(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.TextField()
    nom_alt = models.TextField(blank=True, null=True)
    fecha_pub = models.CharField(max_length=10, blank=True, null=True)
    composicion_orig = models.ForeignKey('self', models.DO_NOTHING, db_column='composicion_orig', blank=True, null=True)
    texto = models.TextField(blank=True, null=True)
    cargador = models.ForeignKey('Participante', models.DO_NOTHING, related_name='composicion_uploader')
    mod = models.ForeignKey('Usuario', models.DO_NOTHING, blank=True, null=True, related_name='mod')
    idiomas = models.ManyToManyField('Idioma', through='IdiomaComposicion')
    participantes = models.ManyToManyField('Participante', through='ParticipanteComposicion',
                                           through_fields=('composicion','part'))
    estado = models.CharField(
        max_length=25,
        choices=RELEASE_STATES_CHOICES,
        default=PENDING,
    )
    temas = models.ManyToManyField('Tema', through='TemaComposicion')

    class Meta:
        managed = True
        db_table = 'composicion'


class FamiliaInstrumento(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.TextField(unique=True)

    class Meta:
        managed = True
        db_table = 'familia_instrumento'


class GeneroMusical(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.TextField(unique=True)
    coment = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'genero_musical'


class GeneroPersona(models.Model):
    nom_genero = models.TextField(primary_key=True)

    class Meta:
        managed = True
        db_table = 'genero_persona'


class GeneroPista(models.Model):
    pista_son = models.ForeignKey('PistaSon', models.DO_NOTHING)
    gen_mus = models.ForeignKey(GeneroMusical, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'genero_pista'
        unique_together = (('pista_son', 'gen_mus'),)


class Grupo(models.Model):
    part = models.OneToOneField('Participante', on_delete=models.CASCADE, primary_key=True)
    tipo_grupo = models.ForeignKey('TipoGrupo', models.DO_NOTHING, db_column='tipo_grupo', blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    nom_part = models.TextField(blank=True, null=True)

    city_of_origin = models.TextField(blank=True, null=True)
    subdivision_of_origin = models.TextField(blank=True, null=True)
    country_of_origin = models.TextField(blank=True, null=True)

    sitio_web = models.URLField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    telefono = models.TextField(blank=True, null=True)
    fecha_comienzo = models.CharField(max_length=10, blank=True, null=True)
    fecha_finale = models.CharField(max_length=10, blank=True, null=True)
    coment_part = models.TextField(blank=True, null=True)
    cargador = models.ForeignKey('Participante', models.DO_NOTHING, related_name='grupo_uploader')
    mod = models.ForeignKey('Usuario', models.DO_NOTHING, blank=True, null=True)
    estado = models.CharField(
        max_length=25,
        choices=RELEASE_STATES_CHOICES,
        default=PENDING,
    )
    personas = models.ManyToManyField('Persona', through='PersonaGrupo')

    class Meta:
        managed = True
        db_table = 'grupo'


class Idioma(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.TextField(unique=True)

    class Meta:
        managed = True
        db_table = 'idioma'


class IdiomaComposicion(models.Model):
    composicion = models.ForeignKey(Composicion, on_delete=models.CASCADE)
    idioma = models.ForeignKey(Idioma, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'idioma_composicion'
        unique_together = (('composicion', 'idioma'),)


class Instrumento(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.TextField()
    familia_instr = models.ForeignKey(FamiliaInstrumento, models.DO_NOTHING, blank=True, null=True)
    electronico = models.NullBooleanField()
    instrumento_comentario = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'instrumento'


class Medio(models.Model):
    nom_medio = models.TextField(primary_key=True)

    class Meta:
        managed = True
        db_table = 'medio'


class Pais(models.Model):
    nom_pais = models.TextField(primary_key=True)

    class Meta:
        managed = True
        db_table = 'pais'


class Participante(models.Model):
    part_id = models.AutoField(primary_key=True)
    coberturas = models.ManyToManyField(Cobertura, through='ParticipanteCobertura')

    class Meta:
        managed = True
        db_table = 'participante'


class ParticipanteCobertura(models.Model):
    cobertura = models.ForeignKey(Cobertura, on_delete=models.CASCADE)
    part = models.ForeignKey(Participante, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'participante_cobertura'
        unique_together = (('cobertura', 'part'),)


class ParticipanteComposicion(models.Model):
    composicion = models.ForeignKey(Composicion, on_delete=models.CASCADE)
    part = models.ForeignKey(Participante, on_delete=models.CASCADE)
    rol_composicion = models.ForeignKey('RolComposicion', models.DO_NOTHING, db_column='rol_composicion')
    datos_personalizados = models.TextField(blank=True, null=True)  # This field type is a guess.
    cargador = models.ForeignKey(Participante, models.DO_NOTHING, related_name='part_comp_uploader')
    mod = models.ForeignKey('Usuario', models.DO_NOTHING, blank=True, null=True)

    estado = models.CharField(
        max_length=25,
        choices=RELEASE_STATES_CHOICES,
        default=PENDING,
    )

    class Meta:
        managed = True
        db_table = 'participante_composicion'
        unique_together = (('composicion', 'part', 'rol_composicion'),)


class ParticipantePistaSon(models.Model):
    pista_son = models.ForeignKey('PistaSon', models.CASCADE)
    part = models.ForeignKey(Participante, models.CASCADE)
    rol_pista_son = models.ForeignKey('RolPistaSon', models.DO_NOTHING, db_column='rol_pista_son')
    instrumento = models.ForeignKey(Instrumento, models.DO_NOTHING)
    datos_personalizados = models.TextField(blank=True, null=True)  # This field type is a guess.
    cargador = models.ForeignKey(Participante, models.DO_NOTHING, related_name='part_pista_uploader')
    mod = models.ForeignKey('Usuario', models.DO_NOTHING, blank=True, null=True)

    estado = models.CharField(
        max_length=25,
        choices=RELEASE_STATES_CHOICES,
        default=PENDING,
    )

    class Meta:
        managed = True
        db_table = 'participante_pista_son'
        unique_together = (('pista_son', 'part', 'rol_pista_son', 'instrumento'),)


class Permiso(models.Model):
    nom_permiso = models.TextField(primary_key=True)

    class Meta:
        managed = True
        db_table = 'permiso'


class Persona(models.Model):
    part = models.OneToOneField(Participante, on_delete=models.CASCADE, primary_key=True)
    nom_paterno = models.TextField(blank=True, null=True)
    nom_materno = models.TextField(blank=True, null=True)
    seudonimo = models.TextField(blank=True, null=True)
    ruta_foto = models.TextField(blank=True, null=True)

    city_of_origin = models.TextField(blank=True, null=True)
    subdivision_of_origin = models.TextField(blank=True, null=True)
    country_of_origin = models.TextField(blank=True, null=True)

    city_of_death = models.TextField(blank=True, null=True)
    subdivision_of_death = models.TextField(blank=True, null=True)
    country_of_death = models.TextField(blank=True, null=True)

    genero = models.ForeignKey(GeneroPersona, models.DO_NOTHING, db_column='genero', blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    nom_part = models.TextField(blank=True, null=True)
    sitio_web = models.URLField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    telefono = models.TextField(blank=True, null=True)
    fecha_comienzo = models.CharField(max_length=10, blank=True, null=True)
    fecha_finale = models.CharField(max_length=10, blank=True, null=True)
    coment_part = models.TextField(blank=True, null=True)
    cargador = models.ForeignKey(Participante, models.DO_NOTHING, related_name='persona_uploader')
    mod = models.ForeignKey('Usuario', models.DO_NOTHING, blank=True, null=True)

    estado = models.CharField(
        max_length=25,
        choices=RELEASE_STATES_CHOICES,
        default=PENDING,
    )

    class Meta:
        managed = True
        db_table = 'persona'


class PersonaGrupo(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    fecha_comienzo = models.CharField(max_length=10, blank=True, null=True)
    fecha_finale = models.CharField(max_length=10, blank=True, null=True)
    titulo = models.TextField(blank=True, null=True)
    cargador = models.ForeignKey(Participante, models.DO_NOTHING)
    mod = models.ForeignKey('Usuario', models.DO_NOTHING, blank=True, null=True)

    estado = models.CharField(
        max_length=25,
        choices=RELEASE_STATES_CHOICES,
        default=PENDING,
    )

    class Meta:
        managed = True
        db_table = 'persona_grupo'
        unique_together = (('persona', 'grupo'),)


class PistaSon(models.Model):
    DIGITAL = 'Digital'
    CD = 'CD'
    TAPE = 'Cinta'
    VINYL = 'Vinilo'
    MEDIA_CHOICES = (
        (DIGITAL, _('Digital')),
        (CD, _('CD')),
        (TAPE, _('Tape')),
        (VINYL, _('Vinyl')),
    )

    pista_son_id = models.AutoField(primary_key=True)
    numero_de_pista = models.IntegerField(blank=True, null=True)
    composicion = models.ForeignKey(Composicion, models.DO_NOTHING, blank=True, null=True)
    medio = models.CharField(max_length=32, choices=MEDIA_CHOICES, default=DIGITAL)

    city_of_origin = models.TextField(blank=True, null=True)
    subdivision_of_origin = models.TextField(blank=True, null=True)
    country_of_origin = models.TextField(blank=True, null=True)

    serie = models.ForeignKey('Serie', models.DO_NOTHING, blank=True, null=True)
    coment_pista_son = models.TextField(blank=True, null=True)
    fecha_grab = models.CharField(max_length=10, blank=True, null=True)
    fecha_dig = models.CharField(max_length=10, blank=True, null=True)
    fecha_cont = models.CharField(max_length=10, blank=True, null=True)
    cargador = models.ForeignKey('Usuario', models.DO_NOTHING, related_name='pista_uploader')
    mod = models.ForeignKey('Usuario', models.DO_NOTHING, blank=True, null=True)
    generos = models.ManyToManyField(GeneroMusical, through=GeneroPista)
    participantes = models.ManyToManyField(Participante, through=ParticipantePistaSon,
                                           through_fields=('pista_son', 'part'))

    estado = models.CharField(max_length=25, choices=RELEASE_STATES_CHOICES, default=PENDING)

    class Meta:
        managed = True
        db_table = 'pista_son'


class RolComposicion(models.Model):
    nom_rol_comp = models.TextField(primary_key=True)

    class Meta:
        managed = True
        db_table = 'rol_composicion'


class RolPistaSon(models.Model):
    nom_rol_pista = models.TextField(primary_key=True)

    class Meta:
        managed = True
        db_table = 'rol_pista_son'


class Serie(models.Model):
    id = models.AutoField(primary_key=True, db_column='id')
    nom = models.TextField(db_column='nom')
    giro = models.TextField(blank=True, null=True)
    ruta_foto = models.TextField(blank=True, null=True)
    coment = models.TextField(blank=True, null=True, db_column='coment')
    cargador = models.ForeignKey(Participante, models.DO_NOTHING)
    mod = models.ForeignKey('Usuario', models.DO_NOTHING, blank=True, null=True)
    estado = models.CharField(max_length=25, choices=RELEASE_STATES_CHOICES, default=PENDING)

    class Meta:
        managed = True
        db_table = 'serie'


class Tema(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.TextField(unique=True)

    class Meta:
        managed = True
        db_table = 'tema'


class TemaComposicion(models.Model):
    composicion = models.ForeignKey(Composicion, models.CASCADE)
    tema = models.ForeignKey(Tema, models.CASCADE)

    class Meta:
        managed = True
        db_table = 'tema_composicion'
        unique_together = (('composicion', 'tema'),)


class TipoGrupo(models.Model):
    nom_tipo_grupo = models.TextField(primary_key=True)

    class Meta:
        managed = True
        db_table = 'tipo_grupo'


class Usuario(models.Model):
    usuario = models.OneToOneField(Participante, models.DO_NOTHING, primary_key=True)
    confirmado = models.BooleanField()
    nom_usuario = models.TextField(unique=True)
    contrasena = models.TextField()
    gr_email = models.OneToOneField(Grupo, models.PROTECT, db_column='gr_email', unique=True, blank=True, null=True)
    pers_email = models.OneToOneField(Persona, models.PROTECT, db_column='pers_email', unique=True, blank=True, null=True)
    fecha_registro = models.DateTimeField(blank=True, null=True)
    fecha_confirmado = models.DateTimeField(blank=True, null=True)
    permiso = models.ForeignKey(Permiso, models.DO_NOTHING, db_column='permiso')
    prohibido = models.BooleanField()

    class Meta:
        managed = True
        db_table = 'usuario'
