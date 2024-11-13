from django.contrib import admin
from django.utils import timezone
from .models import Horario

class HorarioAdmin(admin.ModelAdmin):
    list_display = ['cancha', 'dia', 'hora_inicio', 'hora_fin']
    list_filter = ['dia', 'cancha']  # Filtros para facilitar la administración
    search_fields = ['cancha__nombre']  # Búsqueda por nombre de la cancha
    
    def save_model(self, request, obj, form, change):
        # Validación personalizada en el admin al guardar un horario
        if obj.dia < timezone.now().date() or (obj.dia == timezone.now().date() and obj.hora_inicio <= timezone.now().time()):
            self.message_user(request, "El horario debe ser en una fecha y hora futuras.", level='error')
        else:
            super().save_model(request, obj, form, change)

admin.site.register(Horario, HorarioAdmin)