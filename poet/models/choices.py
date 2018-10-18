from django.utils.translation import gettext_lazy as _
from django.db import models

PUBLISHED = 'PUBLICADO'
DEPOSITED = 'DEPOSITAR'
REJECTED = 'REJECTED'
PENDING = 'PENDIENTE'
RELEASE_STATES_CHOICES = (
    (PUBLISHED, _('Published')),
    (DEPOSITED, _('Deposited')),
    (PENDING, _('Pending')),
    (REJECTED, _('Rejected')),
)


class ReleaseState(models.Model):
    release_state = models.CharField(max_length=128, choices=RELEASE_STATES_CHOICES, primary_key=True,
                                     db_column='release_state')

    class Meta:
        managed = True
        db_table = 'poet_release_state'
