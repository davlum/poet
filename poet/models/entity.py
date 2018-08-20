from django.db import models
from poet.models.choices import RELEASE_STATES_CHOICES, PENDING
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from django.contrib.postgres.fields import JSONField
from poet.models.work import Work


class Entity(models.Model):

    PERSON = 'Persona'
    GROUP = 'Grupo'
    ORGANISATION = 'Organización'
    FESTIVAL = 'Festival'
    UNIVERSITY = 'Universidad'
    COLLECTIVE = 'Colectivo'
    RADIO_STATION = 'Estación radiofónica'
    EDUCATION_AND_RESEARCH = 'Educación e investigación'
    AUDIO_ARCHIVE = 'Archivo sonoro'
    STREAMING_SERVICE = 'Servicios de streaming'
    MUSEUM = 'Museo'
    EDITORIAL = 'Editorial'
    RECORD_LABEL = 'Sello discográfico'
    CULTURAL_CENTER = 'Centro cultural'
    BAND = 'Banda musical'

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

    name = models.TextField()
    alt_name = models.TextField()

    type = models.CharField(max_length=32, choices=ENTITY_TYPE, default=PERSON)

    from_date = models.DateField()
    to_date = models.DateField()

    from_date_end = models.DateField()
    to_date_end = models.DateField()

    city = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)

    website = models.URLField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone_number = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)

    file_path = models.FilePathField()

    tags = ArrayField(models.CharField(max_length=200), blank=True)

    # Arbitrary additional information
    comments = models.TextField()
    data = JSONField()
    history = HistoricalRecords()

    work_relation = models.ManyToManyField(Work, blank=True, symmetrical=False, through='EntityToWorkRel')

    self_relation = models.ManyToManyField('self', blank=True, symmetrical=False, through='EntityToEntityRel')

    state = models.CharField(max_length=32, choices=RELEASE_STATES_CHOICES, default=PENDING)

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

    from_date = models.DateField()
    to_date = models.DateField()

    from_date_end = models.DateField()
    to_date_end = models.DateField()

    # Arbitrary additional information
    comment = models.TextField(blank=True, null=True)
    data = JSONField()
    history = HistoricalRecords()

    class Meta:
        managed = True
        db_table = 'poet_entity_to_entity_rel'
