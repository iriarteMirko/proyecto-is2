from django.contrib import admin
from .models import Cancha

class CanchaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'get_direccion', 'disponibilidad', 'responsable', 'fecha_creacion', 'ultima_modificacion', 'slug']
    prepopulated_fields = {'slug': ('nombre',)}
    readonly_fields = ['fecha_creacion', 'ultima_modificacion']
    
    def get_direccion(self, obj):
        return f'{obj.direccion.tipo_calle} {obj.direccion.nombre_calle}, {obj.direccion.numero_calle}, {obj.direccion.get_distrito_display()}'
    
    get_direccion.short_description = 'Dirección'

admin.site.register(Cancha, CanchaAdmin)