from django.contrib import admin
from .models import Horario

class HorarioAdmin(admin.ModelAdmin):
    list_display = ['cancha', 'fecha', 'hora_inicio', 'hora_fin', 'disponible']
    list_filter = ['cancha', 'fecha', 'disponible']
    search_fields = ['cancha__nombre', 'fecha']

admin.site.register(Horario, HorarioAdmin)