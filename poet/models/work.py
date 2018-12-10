from django.db import models
from poet.models.choices import PENDING, RELEASE_STATES_CHOICES, validate_date
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
import poet.view_contexts.util as u
from simple_history.models import HistoricalRecords
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
import io


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


class WorkCollection(models.Model):

    work_name = models.CharField(max_length=256, blank=True)

    image = models.ImageField(max_length=512, upload_to='images/upload_date=%Y%m%d', null=True)

    commentary = models.TextField(blank=True, null=True)
    additional_data = JSONField(blank=True, null=True)
    history = HistoricalRecords()

    release_state = models.CharField(max_length=32, choices=RELEASE_STATES_CHOICES, default=PENDING,
                                     db_column='release_state')

    class Meta:
        managed = True
        db_table = 'poet_work_collection'


class Work(models.Model):
    """
    Model representing an abstract work, be it a recording, composition,
    album
    """

    full_name = models.CharField(max_length=256, blank=True, null=True)
    alt_name = models.CharField(max_length=128, blank=True, null=True)

    city = models.CharField(max_length=128, blank=True, null=True)
    country = models.CharField(max_length=128, blank=True, null=True)

    audio = models.FileField(max_length=512, upload_to='audio/upload_date=%Y%m%d')

    waveform_peaks = ArrayField(models.FloatField(), editable=False, default=list)

    tags = ArrayField(models.CharField(max_length=256), blank=True, default=list, null=True)

    commentary = models.TextField(blank=True, null=True)
    additional_data = JSONField(blank=True, null=True)
    history = HistoricalRecords()

    in_collection = models.ForeignKey(WorkCollection, null=True, on_delete=models.PROTECT, db_column='in_collection')

    track_number = models.IntegerField(blank=True, null=True)

    release_state = models.CharField(max_length=32, choices=RELEASE_STATES_CHOICES, default=PENDING, db_column='release_state')

    languages = ArrayField(models.CharField(max_length=128), blank=True, default=list, null=True)

    date_published = models.CharField(max_length=10, blank=True, null=True)
    date_digitalized = models.CharField(max_length=10, blank=True, null=True)
    date_recorded = models.CharField(max_length=10, blank=True, null=True)
    date_contributed = models.CharField(max_length=10, blank=True, null=True)

    media_of_origin = models.CharField(max_length=20, choices=MEDIA_CHOICES, default=DIGITAL, blank=True, null=True)

    copyright = models.CharField(max_length=128, blank=True, null=True)
    copyright_country = models.CharField(max_length=150, blank=True, null=True)
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
        buf = io.BytesIO(self.audio.file.read())
        codec = u.get_extension(self.audio.file.name)
        peaks = u.get_peaks_from_audio_path(buf, codec)
        self.waveform_peaks = peaks
        super(Work, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'poet_work'
