from app.models.work import Work
from app.models.entity import Entity
from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from django.contrib.postgres.fields import JSONField

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
    (COMPOSER, COMPOSER),
    (READER, READER),
    (MUSICIAN, MUSICIAN),
    (SOUND_ENGINEER, SOUND_ENGINEER),
    (PRODUCTION, PRODUCTION),
    (DIRECTION, DIRECTION),
    (POST_PRODUCTION, POST_PRODUCTION),
    (AUX, AUX),
    (CONTRIBUTOR, CONTRIBUTOR),
    (PUBLISHER, PUBLISHER),
    (TRANSLATOR, PUBLISHER),
)


class EntityToWorkRel(models.Model):
    from_entity = models.ForeignKey(Entity, on_delete=models.CASCADE, db_column='from_entity', related_name='ew_from_model')
    to_work = models.ForeignKey(Work, on_delete=models.CASCADE, db_column='to_work', related_name='ew_to_model')

    relationship = models.CharField(max_length=256, choices=ENTITY_WORK_ROLE, default=READER)
    # Arbitrary additional information
    commentary = models.TextField(blank=True, null=True)
    additional_data = JSONField(blank=True, null=True)
    history = HistoricalRecords()

    class Meta:
        managed = True
        db_table = 'poet_entity_to_work_rel'



