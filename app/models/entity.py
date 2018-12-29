from django.db import models
from app.models.choices import PENDING, RELEASE_STATES_CHOICES, validate_date
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from app.models.work import Work


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
    (PERSON, PERSON),
    (GROUP, GROUP),
    (ORGANISATION, ORGANISATION),
    (FESTIVAL, FESTIVAL),
    (UNIVERSITY, UNIVERSITY),
    (COLLECTIVE, COLLECTIVE),
    (RADIO_STATION, RADIO_STATION),
    (EDUCATION_AND_RESEARCH, EDUCATION_AND_RESEARCH),
    (AUDIO_ARCHIVE, AUDIO_ARCHIVE),
    (STREAMING_SERVICE, STREAMING_SERVICE),
    (MUSEUM, MUSEUM),
    (EDITORIAL, EDITORIAL),
    (RECORD_LABEL, RECORD_LABEL),
    (CULTURAL_CENTER, CULTURAL_CENTER),
    (BAND, BAND),
)


class Entity(models.Model):

    full_name = models.CharField(max_length=256, blank=True, null=True)
    alt_name = models.CharField(max_length=128, blank=True, null=True)

    entity_type = models.CharField(max_length=128, choices=ENTITY_TYPE, default=PERSON, db_column='entity_type')

    city = models.CharField(max_length=128, blank=True, null=True)
    country = models.CharField(max_length=128, blank=True, null=True)

    email = models.EmailField(blank=True, null=True)

    # Arbitrary additional information
    commentary = models.TextField(blank=True, null=True)
    additional_data = JSONField(blank=True, null=True)
    history = HistoricalRecords()

    start_date = models.CharField(max_length=10, blank=True, null=True)
    end_date = models.CharField(max_length=10, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    address = models.CharField(max_length=256, blank=True, null=True)
    email_address = models.EmailField(blank=True, null=True)

    work_relation = models.ManyToManyField(Work, blank=True, symmetrical=False, through='EntityToWorkRel')

    self_relation = models.ManyToManyField('self', blank=True, symmetrical=False, through='EntityToEntityRel')

    release_state = models.CharField(max_length=32, choices=RELEASE_STATES_CHOICES, default=PENDING, db_column='release_state')

    def clean(self, *args, **kwargs):
        try:
            validate_date(self.end_date)
            validate_date(self.start_date)
        except ValueError as e:
            raise ValidationError(e)

        super(Entity, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Entity, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'poet_entity'


class EntityToEntityRel(models.Model):
    """

    Recursive many to many relationship with the Entity model.
    """

    from_entity = models.ForeignKey(Entity, on_delete=models.CASCADE, db_column='from_entity', related_name='ee_from_model')
    to_entity = models.ForeignKey(Entity, on_delete=models.CASCADE, db_column='to_entity', related_name='ee_to_model')
    contains = models.BooleanField(_('Consists of'), default=False)

    relationship = models.CharField(max_length=256, blank=True, null=True)

    start_date = models.CharField(max_length=10, blank=True, null=True)
    end_date = models.CharField(max_length=10, blank=True, null=True)

    # Arbitrary additional information
    commentary = models.TextField(blank=True, null=True)
    additional_data = JSONField(blank=True, null=True)
    history = HistoricalRecords()

    def clean(self, *args, **kwargs):
        try:
            validate_date(self.end_date)
            validate_date(self.start_date)
        except ValueError as e:
            raise ValidationError(e)

        super(EntityToEntityRel, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(EntityToEntityRel, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'poet_entity_to_entity_rel'
