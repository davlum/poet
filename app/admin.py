from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from app.models.work import Work, WorkCollection
from app.models.entity import Entity, EntityToEntityRel
from app.models.relations import EntityToWorkRel
# Register your models here.


admin.site.register(Entity, SimpleHistoryAdmin)
admin.site.register(EntityToEntityRel, SimpleHistoryAdmin)
admin.site.register(Work, SimpleHistoryAdmin)
admin.site.register(WorkCollection, SimpleHistoryAdmin)
admin.site.register(EntityToWorkRel, SimpleHistoryAdmin)
