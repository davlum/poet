from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from poet.models.work import Work, WorkToWorkRel
from poet.models.entity import Entity, EntityToEntityRel
from poet.models.relations import EntityToWorkRel
# Register your models here.


admin.site.register(Entity, SimpleHistoryAdmin)
admin.site.register(EntityToEntityRel, SimpleHistoryAdmin)
admin.site.register(Work, SimpleHistoryAdmin)
admin.site.register(WorkToWorkRel, SimpleHistoryAdmin)
admin.site.register(EntityToWorkRel, SimpleHistoryAdmin)
