from django.utils.translation import gettext_lazy as _
from django.db import models

PUBLISHED = 'PUBLICADO'
DEPOSITED = 'DEPOSITAR'
REJECTED = 'RECHAZADO'
PENDING = 'PENDIENTE'
RELEASE_STATES_CHOICES = (
    (PUBLISHED, _('Published')),
    (DEPOSITED, _('Deposited')),
    (PENDING, _('Pending')),
    (REJECTED, _('Rejected')),
)
