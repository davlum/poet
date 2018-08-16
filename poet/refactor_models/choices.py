from django.utils.translation import gettext_lazy as _

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