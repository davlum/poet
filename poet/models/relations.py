from poet.models.work import Work
from poet.models.entity import Entity
from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from django.contrib.postgres.fields import JSONField


class EntityToWorkRel(models.Model):
    READER = 'Lectura en voz alta'
    MUSICIAN = 'Interpretación musical'
    SOUND_ENGINEER = 'Ingeniería de sonido'
    PRODUCTION = 'Producción'
    DIRECTION = 'Dirección'
    POST_PRODUCTION = 'Post-producción'
    AUX = 'Auxiliar de sonido'
    CONTRIBUTOR = 'Contribuidor'
    PUBLISHER = 'Publicador'
    COMPOSER = 'Composición'
    TRANSLATOR = 'Traducción'
    ENTITY_WORK_ROLE = (
       (READER, _('Lectura en voz alta')),
       (MUSICIAN, _('Interpretación musical')),
       (SOUND_ENGINEER, _('Ingeniería de sonido')),
       (PRODUCTION, _('Producción')),
       (DIRECTION, _('Dirección')),
       (POST_PRODUCTION, _('Post-producción')),
       (AUX, _('Auxiliar de sonido')),
       (CONTRIBUTOR, _('Contribuidor')),
       (PUBLISHER, _('Publicador')),
       (COMPOSER, _('Composición')),
       (TRANSLATOR, _('Traducción')),
    )

    from_model = models.ForeignKey(Entity, on_delete=models.CASCADE)
    to_model = models.ForeignKey(Work, on_delete=models.CASCADE)

    role = models.CharField(max_length=128, choices=ENTITY_WORK_ROLE)
    # Arbitrary additional information
    comments = models.TextField(blank=True, null=True)
    additional_data = JSONField(blank=True, null=True)
    history = HistoricalRecords()

    class Meta:
        managed = True
        db_table = 'poet_entity_to_work_rel'
