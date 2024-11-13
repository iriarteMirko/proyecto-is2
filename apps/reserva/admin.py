from django.contrib import admin
from .models import Reserva

class ReservaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'horario', 'hora_reserva_inicio', 'hora_reserva_fin', 'fecha_reserva']
    list_filter = ['fecha_reserva', 'horario__cancha']  # Filtros por fecha y cancha
    search_fields = ['usuario__email', 'horario__cancha__nombre']  # Búsqueda por usuario y nombre de la cancha
    
    def save_model(self, request, obj, form, change):
        # Validación personalizada en el admin para evitar conflictos de reserva
        if Reserva.objects.filter(
            horario__cancha=obj.horario.cancha,
            horario__dia=obj.horario.dia,
            hora_reserva_inicio__lt=obj.hora_reserva_fin,
            hora_reserva_fin__gt=obj.hora_reserva_inicio
        ).exclude(id=obj.id).exists():
            self.message_user(request, "Este horario ya está reservado. Elige otro.", level='error')
        else:
            super().save_model(request, obj, form, change)

admin.site.register(Reserva, ReservaAdmin)