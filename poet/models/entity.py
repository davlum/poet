from django.db import models
from poet.models.choices import RELEASE_STATES_CHOICES, PENDING
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from django.contrib.postgres.fields import JSONField
from poet.models.work import Work


class Entity(models.Model):

    PERSON = 'PERSONA'
    GROUP = 'GRUPO'
    ORGANISATION = 'ORGANIZACIÓN'
    FESTIVAL = 'FESTIVAL'
    UNIVERSITY = 'UNIVERSIDAD'
    COLLECTIVE = 'COLECTIVO'
    RADIO_STATION = 'ESTACIÓN RADIOFÓNICA'
    EDUCATION_AND_RESEARCH = 'EDUCACIÓN E INVESTIGACIÓN'
    AUDIO_ARCHIVE = 'ARCHIVO SONORO'
    STREAMING_SERVICE = 'SERVICIOS DE STREAMING'
    MUSEUM = 'MUSEO'
    EDITORIAL = 'EDITORIAL'
    RECORD_LABEL = 'SELLO DISCOGRÁFICO'
    CULTURAL_CENTER = 'CENTRO CULTURAL'
    BAND = 'BANDA MUSICAL'

    ENTITY_TYPE = (
        (PERSON, _('Persona')),
        (GROUP, _('Grupo')),
        (ORGANISATION, _('Organización')),
        (FESTIVAL, _('Festival')),
        (UNIVERSITY, _('Universidad')),
        (COLLECTIVE, _('Colectivo')),
        (RADIO_STATION, _('Estación radiofónica')),
        (EDUCATION_AND_RESEARCH, _('Educación e investigación')),
        (AUDIO_ARCHIVE, _('Archivo sonoro')),
        (STREAMING_SERVICE, _('Servicios de streaming')),
        (MUSEUM, _('Museo')),
        (EDITORIAL, _('Editorial')),
        (RECORD_LABEL, _('Sello discográfico')),
        (CULTURAL_CENTER, _('Centro cultural')),
        (BAND, _('Banda musical')),
    )

    full_name = models.TextField(blank=True, null=True)
    alt_name = models.TextField(blank=True, null=True)

    entity_type = models.CharField(max_length=32, choices=ENTITY_TYPE, default=PERSON)

    from_date = models.DateField(blank=True, null=True)
    to_date = models.DateField(blank=True, null=True)

    from_date_end = models.DateField(blank=True, null=True)
    to_date_end = models.DateField(blank=True, null=True)

    city = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)

    email = models.EmailField(blank=True, null=True)

    file_path = models.FilePathField(blank=True, null=True)

    tags = ArrayField(models.CharField(max_length=200), blank=True, default=list, null=True)

    # Arbitrary additional information
    comments = models.TextField(blank=True, null=True)
    additional_data = JSONField(blank=True, null=True)
    history = HistoricalRecords()

    work_relation = models.ManyToManyField(Work, blank=True, symmetrical=False, through='EntityToWorkRel')

    self_relation = models.ManyToManyField('self', blank=True, symmetrical=False, through='EntityToEntityRel')

    release_state = models.CharField(max_length=32, choices=RELEASE_STATES_CHOICES, default=PENDING)

    class Meta:
        managed = True
        db_table = 'poet_entity'


class EntityToEntityRel(models.Model):
    """

    Recursive many to many relationship with the Entity model.
    """

    from_model = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='from_entity')
    to_model = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='to_entity')
    contains = models.BooleanField(_('Is part of'), default=False)

    role = models.TextField(blank=True, null=True)

    from_date = models.DateField(blank=True, null=True)
    to_date = models.DateField(blank=True, null=True)

    from_date_end = models.DateField(blank=True, null=True)
    to_date_end = models.DateField(blank=True, null=True)

    # Arbitrary additional information
    comment = models.TextField(blank=True, null=True)
    additional_data = JSONField(blank=True, null=True)
    history = HistoricalRecords()

    class Meta:
        managed = True
        db_table = 'poet_entity_to_entity_rel'
