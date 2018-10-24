from poet.models.work import Work
from poet.models.entity import Entity
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


class EntityToWorkRole(models.Model):
    role_type = models.CharField(max_length=128, primary_key=True)

    class Meta:
        managed = True
        db_table = 'poet_entity_to_work_role'


class EntityToWorkRel(models.Model):
    from_entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='ew_from_model')
    to_work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='ew_to_model')

    role = models.ForeignKey(EntityToWorkRole, on_delete=models.PROTECT)
    # Arbitrary additional information
    commentary = models.TextField(blank=True, null=True)
    additional_data = JSONField(blank=True, null=True)
    history = HistoricalRecords()

    class Meta:
        managed = True
        db_table = 'poet_entity_to_work_rel'



