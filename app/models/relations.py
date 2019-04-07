from django.db import models
from django.utils.translation import gettext, gettext_lazy as _
from simple_history.models import HistoricalRecords
from django.core.exceptions import ValidationError

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
    (TRANSLATOR, TRANSLATOR),
)


class EntityToWorkRel(models.Model):
    from_entity = models.ForeignKey('Entity', verbose_name=_('From entity'), on_delete=models.CASCADE,
                                    db_column='from_entity', related_name='ew_from_model')
    to_work = models.ForeignKey('Work', verbose_name=_('To recording'), on_delete=models.CASCADE,
                                db_column='to_work', related_name='ew_to_model')

    relationship = models.CharField(max_length=256, verbose_name=_('Role'), choices=ENTITY_WORK_ROLE, default=READER)
    instrument = models.CharField(max_length=256, verbose_name=_('Instrument'), blank=True, null=True)

    # Arbitrary additional information
    commentary = models.TextField(verbose_name=_('Additional commentary'), blank=True, null=True)
    history = HistoricalRecords()

    def clean(self, *args, **kwargs):
        if self.relationship == MUSICIAN and (self.instrument is None or self.instrument.strip() == ''):
            raise ValidationError(gettext('Must select an instrument if role is interpretation'))
        if self.relationship != MUSICIAN and (self.instrument is not None or self.instrument.strip() != ''):
            raise ValidationError(gettext('Must not select an instrument if role is not interpretation'))
        super(EntityToWorkRel, self).clean(*args, **kwargs)

    def __str__(self):
        return gettext("Relation from {from_entity} to {to_work}").format(
            from_entity=self.from_entity,
            to_work=self.to_work
        )

    class Meta:
        managed = True
        db_table = 'poet_entity_to_work_rel'
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')



