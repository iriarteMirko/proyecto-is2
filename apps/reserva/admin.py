from django.contrib import admin
from .models import Reserva

class ReservaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'horario', 'fecha_reserva']
    list_filter = ['fecha_reserva', 'usuario']
    search_fields = ['usuario__email', 'horario__cancha__nombre', 'horario__fecha']

admin.site.register(Reserva, ReservaAdmin)