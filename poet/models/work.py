from django.db import models
from poet.models.choices import RELEASE_STATES_CHOICES, PENDING
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from django.contrib.postgres.fields import JSONField


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

    # This should be types of works. Media types are additional data
    type = models.CharField(max_length=32, choices=WORK_TYPE, default=RECORDING)

    from_date = models.DateField()
    to_date = models.DateField()

    city = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)

    path_to_file = models.FilePathField()
    file_type = models.CharField(max_length=25, choices=FILE_TYPE, default=PENDING)

    tags = ArrayField(models.CharField(max_length=200), blank=True)

    comments = models.TextField()
    data = JSONField()
    history = HistoricalRecords()

    self_relation = models.ManyToManyField('self', blank=True, symmetrical=False, through='WorkToWorkRel')

    state = models.CharField(max_length=32, choices=RELEASE_STATES_CHOICES, default=PENDING)

    class Meta:
        managed = True
        db_table = 'poet_work'


class WorkToWorkRel(models.Model):
    """

    Recursive many to many relationship with the Work model.
    """

    from_model = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='from_work')
    to_model = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='to_work')
    contains = models.BooleanField(_('Is part of'), default=False)
    order = models.IntegerField(blank=True, null=True)
    role = models.TextField(blank=True, null=True)
    # Arbitrary additional information
    comment = models.TextField(blank=True, null=True)
    data = JSONField()
    history = HistoricalRecords()

    class Meta:
        managed = True
        db_table = 'poet_work_to_work_rel'


