from django.db import models
from poet.refactor_models.choices import RELEASE_STATES_CHOICES, PENDING
from django.utils.translation import gettext as _
from simple_history.models import HistoricalRecords
from django.contrib.postgres.fields import JSONField

ALBUM = 'ALBUM'
SERIES = 'SERIE'
COLLECTION_TYPE = (
    (ALBUM, _('Album')),
    (SERIES, _('Series')),
)


class Collection(models.Model):
    """
    This class is the abstract notion of a collection of works. From the original schema,
    this is both the album and serie entity in one
    """
    name = models.TextField(blank=True, null=True)
    relation = models.ManyToManyField('self', blank=True, null=True, symmetrical=False, through='CollectionRelation')
    photo = models.FileField()
    comments = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=32, choic=COLLECTION_TYPE, default=SERIES)
    state = models.CharField(max_length=32, choices=RELEASE_STATES_CHOICES, default=PENDING)
    history = HistoricalRecords()

    class Meta:
        managed = True
        db_table = 'poet_collection'


class CollectionRelation(models.Model):
    subsumer = models.ForeignKey(Collection, on_delete=models.CASCADE)
    subsumed = models.ForeignKey(Collection, on_delete=models.CASCADE)
    order = models.IntegerField(blank=True, null=True)
    # Arbitrary additional information
    comment = models.TextField(blank=True, null=True)
    data = JSONField()

    class Meta:
        managed = True
        db_table = 'poet_collection_relations'

