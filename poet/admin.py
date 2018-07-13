from django.contrib import admin

# Register your models here.

from .models import PistaSon, Cobertura, Composicion, Persona, Grupo

admin.site.register(PistaSon)
admin.site.register(Cobertura)
admin.site.register(Composicion)
admin.site.register(Persona)
admin.site.register(Grupo)
