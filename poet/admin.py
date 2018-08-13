from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
# Register your models here.

from .models import PistaSon, Cobertura, Composicion, Persona, Grupo

admin.site.register(PistaSon, SimpleHistoryAdmin)
admin.site.register(Cobertura, SimpleHistoryAdmin)
admin.site.register(Composicion, SimpleHistoryAdmin)
admin.site.register(Persona, SimpleHistoryAdmin)
admin.site.register(Grupo, SimpleHistoryAdmin)
