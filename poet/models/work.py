from django.db import models
from poet.models.choices import ReleaseState, PENDING
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from django.contrib.postgres.fields import JSONField

SERIES = 'SERIES'
RECORDING = 'RECORDING'
WORK_TYPE = (
    (SERIES, _('Series')),
    (RECORDING, _('Recording')),
)


class WorkType(models.Model):
    work_type = models.CharField(max_length=128, primary_key=True)

    class Meta:
        managed = True
        db_table = 'poet_work_type'


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

    IMAGE = 'IMAGE'
    AUDIO = 'AUDIO'
    FILE_TYPE = (
        (AUDIO, _('Audio')),
        (IMAGE, _('Image'))
    )

    full_name = models.TextField(blank=True, null=True)
    alt_name = models.TextField(blank=True, null=True)

    # This should be types of works. Media types are additional data
    work_type = models.ForeignKey(WorkType, on_delete=models.PROTECT, db_column='work_type')

    from_date = models.DateField(blank=True, null=True)
    to_date = models.DateField(blank=True, null=True)

    city = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)

    path_to_file = models.FilePathField(blank=True, null=True)
    file_type = models.CharField(max_length=25, choices=FILE_TYPE, null=True)

    tags = ArrayField(models.CharField(max_length=200), blank=True, default=list, null=True)

    commentary = models.TextField(blank=True, null=True)
    additional_data = JSONField(blank=True, null=True)
    history = HistoricalRecords()

    self_relation = models.ManyToManyField('self', blank=True, symmetrical=False, through='WorkToWorkRel')

    release_state = models.ForeignKey(ReleaseState, on_delete=models.PROTECT, default=PENDING, db_column='release_state')

    copyright = models.TextField(blank=True, null=True)
    copyright_country = models.TextField(blank=True, null=True)
    copyright_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'poet_work'


class WorkToWorkRel(models.Model):
    """

    Recursive many to many relationship with the Work model.
    """

    from_work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='ww_from_model')
    to_work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='ww_to_model')
    contains = models.BooleanField(_('Consists of'), default=False)
    order = models.IntegerField(blank=True, null=True)
    role = models.TextField(blank=True, null=True, db_column='role_id')
    # Arbitrary additional information
    commentary = models.TextField(blank=True, null=True)
    additional_data = JSONField(blank=True, null=True)
    history = HistoricalRecords()

    class Meta:
        managed = True
        db_table = 'poet_work_to_work_rel'
