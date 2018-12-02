from django.utils.translation import gettext_lazy as _
from datetime import datetime
import re

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


def validate_date(date):
    bad_format = _('Date does not match format YYYY-MM-DD.')
    bad_date = _('Not a valid date.')
    try:
        if re.match(r'\d{4}-\d{2}-\d{2}', date):
            datetime.strptime(date, '%Y-%m-%d')
            return
        if re.match(r'\d{4}-\d{2}', date):
            datetime.strptime(date, '%Y-%m')
            return
        if re.match(r'\d{4}', date):
            datetime.strptime(date, '%Y')
            return
    except ValueError:
        raise ValueError(bad_date)
    raise ValueError(bad_format)
