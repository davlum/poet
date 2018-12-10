from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from poet.models.work import Work, WorkCollection
from poet.models.entity import Entity, EntityToEntityRel
from poet.models.relations import EntityToWorkRel
# Register your models here.


admin.site.register(Entity, SimpleHistoryAdmin)
admin.site.register(EntityToEntityRel, SimpleHistoryAdmin)
admin.site.register(Work, SimpleHistoryAdmin)
admin.site.register(WorkCollection, SimpleHistoryAdmin)
admin.site.register(EntityToWorkRel, SimpleHistoryAdmin)
