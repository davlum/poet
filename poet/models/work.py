from django.db import models
from poet.models.choices import PENDING, RELEASE_STATES_CHOICES, validate_date
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError

SERIES = 'Serie'
RECORDING = 'Pista son'
WORK_TYPE = (
    (SERIES, SERIES),
    (RECORDING, RECORDING),
)

DIGITAL = 'Digital'
TAPE = 'Cinta'
CD = 'CD'
VINYL = 'Vinilo'
MEDIA_CHOICES = (
    (DIGITAL, DIGITAL),
    (TAPE, TAPE),
    (CD, CD),
    (VINYL, VINYL)
)


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

    IMAGE = 'images'
    AUDIO = 'audio'
    FILE_TYPE = (
        (AUDIO, _('Audio')),
        (IMAGE, _('Image'))
    )

    full_name = models.TextField(blank=True, null=True)
    alt_name = models.TextField(blank=True, null=True)

    # This should be types of works. Media types are additional data
    work_type = models.TextField(choices=WORK_TYPE, default=RECORDING, db_column='work_type')

    city = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)

    path_to_file = models.FilePathField(blank=True, null=True)
    file_type = models.CharField(max_length=25, choices=FILE_TYPE, null=True)

    tags = ArrayField(models.CharField(max_length=200), blank=True, default=list, null=True)

    commentary = models.TextField(blank=True, null=True)
    additional_data = JSONField(blank=True, null=True)
    history = HistoricalRecords()

    self_relation = models.ManyToManyField('self', blank=True, symmetrical=False, through='WorkToWorkRel')

    release_state = models.TextField(choices=RELEASE_STATES_CHOICES, default=PENDING, db_column='release_state')

    languages = ArrayField(models.CharField(max_length=200), blank=True, default=list, null=True)

    date_published = models.CharField(max_length=10, blank=True, null=True)
    date_digitalized = models.CharField(max_length=10, blank=True, null=True)
    date_recorded = models.CharField(max_length=10, blank=True, null=True)
    date_contributed = models.CharField(max_length=10, blank=True, null=True)

    media_of_origin = models.CharField(max_length=20, choices=MEDIA_CHOICES, default=DIGITAL, blank=True, null=True)

    copyright = models.TextField(blank=True, null=True)
    copyright_country = models.TextField(blank=True, null=True)
    copyright_date = models.DateField(blank=True, null=True)

    def clean(self, *args, **kwargs):
        try:
            validate_date(self.date_published)
            validate_date(self.date_recorded)
            validate_date(self.date_contributed)
            validate_date(self.date_digitalized)
        except ValueError as e:
            raise ValidationError(e)

        super(Work, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Work, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'poet_work'


SERIES_CONTAINS_RECORDING = 'Series<contains>Recording'
SERIES_CONTAINS_ALBUM = 'Series<contains>Album'
SERIES_INFLUENCED_RECORDING = 'Series<influenced>Recording'

RELATIONSHIP_CHOICES = (
    (SERIES_CONTAINS_ALBUM, _('Is the series which contains this album.')),
    (SERIES_CONTAINS_RECORDING, _('Is the series which contains this track.')),
    (SERIES_INFLUENCED_RECORDING, _('Is a series which influenced this track.'))
)


class WorkToWorkRel(models.Model):
    """
    Recursive many to many relationship with the Work model.
    """

    from_work = models.ForeignKey(Work, on_delete=models.CASCADE, db_column='from_work', related_name='ww_from_model')
    to_work = models.ForeignKey(Work, on_delete=models.CASCADE, db_column='to_work', related_name='ww_to_model')
    contains = models.BooleanField(_('Consists of'), default=False)
    track_order = models.IntegerField(blank=True, null=True)
    relationship = models.TextField(choices=RELATIONSHIP_CHOICES, default=SERIES_CONTAINS_RECORDING, blank=True, null=True)
    # Arbitrary additional information
    commentary = models.TextField(blank=True, null=True)
    additional_data = JSONField(blank=True, null=True)
    history = HistoricalRecords()

    class Meta:
        managed = True
        db_table = 'poet_work_to_work_rel'
