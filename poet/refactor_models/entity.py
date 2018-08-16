from django.db import models
from poet.refactor_models.choices import RELEASE_STATES_CHOICES, PENDING
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from django.contrib.postgres.fields import JSONField


class EntityType(models.Model):
    name = models.TextField()

    class meta:
        db_table = 'poet_entity_type'


class Entity(models.Model):

    PERSON = 'ALBUM'
    GROUP = 'SERIE'
    ORGANISATION = 'COMPOSICION'
    FESTIVAL = 'PISTA SON'
    ENTITY_TYPE = (
        (PERSON, _('Person')),
        (GROUP, _('Group')),
        (ORGANISATION, _('Organization')),
        (FESTIVAL, _('Recording'))
    )

    name = models.TextField()
    alt_name = models.TextField()
    comments = models.TextField()

    type = models.ForeignKey(max_length=32, choices=ENTITY_TYPE, on_delete=models.PROTECT)

    from_date = models.DateField()
    to_date = models.DateField()

    city_of_origin = models.TextField(blank=True, null=True)
    subdivision_of_origin = models.TextField(blank=True, null=True)
    country_of_origin = models.TextField(blank=True, null=True)

    website = models.URLField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone_number = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)

    path_to_file = models.FileField()
    file_type = models.CharField(max_length=25, choices=FILE_TYPE, default=PENDING)

    tags = ArrayField(models.CharField(max_length=200), blank=True)
    data = JSONField()
    history = HistoricalRecords()

    entity_relation = models.ManyToManyField(Entity, symmetrical=False, through='WorkEntity')

    self_relation = models.ManyToManyField('self', blank=True, null=True, symmetrical=False, through='EntityEntity')

    state = models.CharField(max_length=32, choices=RELEASE_STATES_CHOICES, default=PENDING)

    class Meta:
        managed = True
        db_table = 'poet_entity'


class EntityEntity(models.Model):
    """

    Recursive many to many relationship with the Entity model.
    """
    TRANSLATION = 'TRANSLATION'
    INFLUENCED = 'INFLUENCED'
    ENTITY_RELATION_TYPE = (
        (TRANSLATION, _('Translation')),
        (INFLUENCED, _('Influenced')),
    )

    from_model = models.ForeignKey(Entity, on_delete=models.CASCADE)
    to_model = models.ForeignKey(Entity, on_delete=models.CASCADE)
    type = models.CharField(max_length=32, blank=True, null=True, choices=ENTITY_RELATION_TYPE, default=INFLUENCED)

    from_date_start = models.DateField()
    to_date_start = models.DateField()

    from_date_end = models.DateField()
    to_date_end = models.DateField()

    # Arbitrary additional information
    comment = models.TextField(blank=True, null=True)
    data = JSONField()

    class Meta:
        managed = True
        db_table = 'poet_entity_entity'


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

