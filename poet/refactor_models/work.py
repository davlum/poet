from django.db import models
from poet.refactor_models.choices import RELEASE_STATES_CHOICES, PENDING
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from django.contrib.postgres.fields import JSONField
from poet.refactor_models.entity import Entity


class Work(models.Model):
    """

    Model representing an abstract work, be it a recording, composition,
    album

    I believe the path is currently the archivo_id and filename.

    Paths are being used instead of django's built in file type in order
    to easily transition to an external service if necessary (S3 for example).
    in order to refactor to using Django's built in file type see;
    https://www.revsys.com/tidbits/loading-django-files-from-code/

    Future paths will use;
    /<STATIC_DIR>/<MEDIA_TYPE>/<GENERATED_UUID>_<FILENAME>
    """
    ALBUM = 'ALBUM'
    SERIES = 'SERIE'
    COMPOSITION = 'COMPOSICION'
    RECORDING = 'PISTA SON'
    WORK_TYPE = (
        (ALBUM, _('Album')),
        (SERIES, _('Series')),
        (COMPOSITION, _('Composition')),
        (RECORDING, _('Recording'))
    )

    IMAGE = 'IMAGE'
    AUDIO = 'AUDIO'
    FILE_TYPE = (
        (AUDIO, _('Audio')),
        (IMAGE, _('Image'))
    )

    name = models.TextField()
    alt_name = models.TextField()
    comments = models.TextField()
    # This should be types of works. Media types are additional data
    type = models.CharField(max_length=32, choices=WORK_TYPE, default=RECORDING)

    from_date = models.DateField()
    to_date = models.DateField()

    city_of_origin = models.TextField(blank=True, null=True)
    subdivision_of_origin = models.TextField(blank=True, null=True)
    country_of_origin = models.TextField(blank=True, null=True)

    path_to_file = models.FileField()
    file_type = models.CharField(max_length=25, choices=FILE_TYPE, default=PENDING)

    tags = ArrayField(models.CharField(max_length=200), blank=True)
    data = JSONField()
    history = HistoricalRecords()

    entity_relation = models.ManyToManyField(Entity, symmetrical=False, through='WorkEntity')

    self_relation = models.ManyToManyField('self', blank=True, null=True, symmetrical=False, through='WorkWork')

    state = models.CharField(max_length=32, choices=RELEASE_STATES_CHOICES, default=PENDING)

    class Meta:
        managed = True
        db_table = 'poet_work'


class WorkWork(models.Model):
    """

    Recursive many to many relationship with the Work model.
    """
    TRANSLATION = 'TRANSLATION'
    INFLUENCED = 'INFLUENCED'
    WORK_RELATION_TYPE = (
        (TRANSLATION, _('Translation')),
        (INFLUENCED, _('Influenced')),
    )

    from_model = models.ForeignKey(Work, on_delete=models.CASCADE)
    to_model = models.ForeignKey(Work, on_delete=models.CASCADE)
    order = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=32, blank=True, null=True, choices=WORK_RELATION_TYPE, default=INFLUENCED)
    # Arbitrary additional information
    comment = models.TextField(blank=True, null=True)
    data = JSONField()

    class Meta:
        managed = True
        db_table = 'poet_work_work'


