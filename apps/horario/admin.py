from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Horario

class HorarioForm(ModelForm):
    class Meta:
        model = Horario
        fields = ['cancha', 'dia', 'hora_inicio', 'hora_fin']
    
    def clean(self):
        cleaned_data = super().clean()
        horario = Horario(
            cancha=cleaned_data.get('cancha'),
            dia=cleaned_data.get('dia'),
            hora_inicio=cleaned_data.get('hora_inicio'),
            hora_fin=cleaned_data.get('hora_fin'),
        )
        try:
            horario.clean()
        except ValidationError as e:
            self.add_error(None, e)  # Añade el error al formulario
        return cleaned_data

class HorarioAdmin(admin.ModelAdmin):
    form = HorarioForm
    list_display = ['cancha', 'dia', 'hora_inicio', 'hora_fin']
    list_filter = ['cancha', 'dia']
    search_fields = ['cancha__nombre', 'dia']

admin.site.register(Horario, HorarioAdmin)