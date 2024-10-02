from django.contrib import admin
from .models import Usuario

class UsuarioAdmin(admin.ModelAdmin):
    # Campos que se mostrarán en la lista de usuarios en el admin
    list_display = ['email', 'dni', 'nombre', 'apellidos', 'celular', 'is_responsible', 'is_staff', 'is_superuser', 'slug']

admin.site.register(Usuario, UsuarioAdmin)
