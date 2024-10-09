from django.contrib import admin
from .models import Cancha

class CanchaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'ubicacion', 'disponibilidad', 'responsable', 'fecha_creacion', 'ultima_modificacion', 'slug']
    prepopulated_fields = {'slug': ('nombre',)}  # Para generar automáticamente el slug basado en el nombre
    readonly_fields = ['fecha_creacion', 'ultima_modificacion']  # Campos de solo lectura en el admin

admin.site.register(Cancha, CanchaAdmin)