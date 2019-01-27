from django.db import models
from app.models.choices import PENDING, RELEASE_STATES_CHOICES, validate_date
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext, gettext_lazy as _
import app.controllers.util as u
from simple_history.models import HistoricalRecords
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


C = '(C) Copyright'
CC_BY = '(CC BY) Creative Commons Atribución'
CC_BY_SA = '(CC BY-SA) Creative Commons Atribución-CompartirIgual'
CC_BY_NC = '(CC BY-NC) Creative Commons Atribución-NoComercial'
CC_BY_NC_SA = '(CC BY-NC-SA) Creative Commons Atribución-NoComercial-CompartirIgual'
CC_BY_NC_ND = '(CC BY-NC-ND) Creative Commons Atribución-NoComercial-SinDerivadas'
CC0 = '(CC0) Sin derechos reservados'
GPL = '(GPL) Licencia pública general GNU'
LGPL = '(LGPL) Licencia pública menos general GNU'
DOM = 'Dominio público'
PAT = 'Patente'
POR = 'Por confirmar'
LEFT = 'Copyleft'
CC_BY_ND = '(CC BY-ND) Creative Commons Atribución-SinDerivadas'

COPYRIGHT_CHOICES = (
   (C, C),
   (CC_BY, CC_BY),
   (CC_BY_SA, CC_BY_SA),
   (CC_BY_NC, CC_BY_NC),
   (CC_BY_NC_SA, CC_BY_NC_SA),
   (CC_BY_NC_ND, CC_BY_NC_ND),
   (CC0, CC0),
   (GPL, GPL),
   (LGPL, LGPL),
   (DOM, DOM),
   (PAT, PAT),
   (POR, POR),
   (LEFT, LEFT),
   (CC_BY_ND, CC_BY_ND)
)


class WorkCollection(models.Model):

    collection_name = models.CharField(verbose_name=_('Collection title'), max_length=256, blank=True)

    image = models.ImageField(max_length=512, verbose_name=_('Album art'), upload_to='images/upload_date=%Y%m%d', null=True, blank=True)

    album_art_design = models.CharField(max_length=512, verbose_name=_('Album art design'), null=True, blank=True)

    origin = models.CharField(max_length=128, verbose_name=_('Origin'), blank=True, null=True)

    commentary = models.TextField(verbose_name=_('Additional commentary'), blank=True, null=True)
    history = HistoricalRecords()

    release_state = models.CharField(verbose_name=_('State of Publication'), max_length=32,
                                     choices=RELEASE_STATES_CHOICES, default=PENDING, db_column='release_state')

    def __str__(self):
        if self.collection_name is not None and self.collection_name.strip() != '':
            return self.collection_name
        return gettext('Collection {id}').format(id=self.id)

    class Meta:
        managed = True
        db_table = 'poet_work_collection'
        verbose_name = _('Recording collection')
        verbose_name_plural = _('Recording collections')


class Work(models.Model):
    """
    Model representing a recording/composition
    """

    full_name = models.CharField(verbose_name=_('Title'), max_length=256, blank=True, null=True)
    alt_name = models.CharField(verbose_name=_('Alternative title'), max_length=128, blank=True, null=True)

    city = models.CharField(verbose_name=_('City'), max_length=128, blank=True, null=True)
    country = models.CharField(verbose_name=_('Country'), max_length=128, blank=True, null=True)

    audio = models.FileField(verbose_name=_('Recording'), max_length=512, upload_to='audio/upload_date=%Y%m%d')

    waveform_peaks = ArrayField(models.FloatField(), editable=False, default=list)

    tags = ArrayField(models.CharField(max_length=256), verbose_name=_('Tags'), blank=True, default=list)

    external_url = models.URLField(verbose_name=_('External URL'), blank=True, null=True)

    commentary = models.TextField(verbose_name=_('Additional commentary'), blank=True, null=True)
    poetry_text = models.TextField(verbose_name=_('Composition text'), blank=True, null=True)

    history = HistoricalRecords()

    in_collection = models.ForeignKey(WorkCollection, verbose_name=_('Collection that this recording is a part of'),
                                      null=True, on_delete=models.PROTECT, db_column='in_collection')

    track_number = models.IntegerField(verbose_name=_('Track number in that collection'), blank=True, null=True)

    release_state = models.CharField(verbose_name=_('State of Publication'), max_length=32, choices=RELEASE_STATES_CHOICES, default=PENDING, db_column='release_state')

    languages = ArrayField(models.CharField(max_length=128), verbose_name=_('Languages Spoken'), blank=True, default=list, null=True)

    date_published = models.CharField(max_length=10, verbose_name=_('Date published'), blank=True, null=True)
    date_digitalized = models.CharField(max_length=10, verbose_name=_('Date digitized'), blank=True, null=True)
    date_recorded = models.CharField(max_length=10, verbose_name=_('Date recorded'), blank=True, null=True)
    date_contributed = models.CharField(max_length=10, verbose_name=_('Date contributed'), blank=True, null=True)

    media_of_origin = models.CharField(max_length=20, verbose_name=_('Media of origin'), choices=MEDIA_CHOICES,
                                       default=DIGITAL, blank=True, null=True)

    copyright = models.CharField(max_length=128, verbose_name=_('License'), choices=COPYRIGHT_CHOICES, default=CC_BY)
    copyright_country = models.CharField(max_length=150, verbose_name=_('Country of License'), blank=True, null=True)

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

    def __str__(self):
        if self.full_name is not None and self.full_name.strip() != '':
            return self.full_name
        if self.alt_name is not None and self.alt_name.strip() != '':
            return self.alt_name
        return gettext('Recording {id}').format(id=self.id)

    class Meta:
        managed = True
        db_table = 'poet_work'
        verbose_name = _('Recording')
        verbose_name_plural = _('Recordings')
