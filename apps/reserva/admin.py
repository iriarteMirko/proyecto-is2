from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Reserva

class ReservaForm(ModelForm):
    class Meta:
        model = Reserva
        fields = ['usuario', 'horario', 'hora_reserva_inicio', 'hora_reserva_fin']
    
    def clean(self):
        cleaned_data = super().clean()
        reserva = Reserva(
            usuario=cleaned_data.get('usuario'),
            horario=cleaned_data.get('horario'),
            hora_reserva_inicio=cleaned_data.get('hora_reserva_inicio'),
            hora_reserva_fin=cleaned_data.get('hora_reserva_fin'),
        )
        try:
            reserva.clean()
        except ValidationError as e:
            self.add_error(None, e)
        return cleaned_data

class ReservaAdmin(admin.ModelAdmin):
    form = ReservaForm
    list_display = ['usuario', 'horario', 'hora_reserva_inicio', 'hora_reserva_fin', 'fecha_reserva']
    list_filter = ['horario__cancha', 'horario__dia', 'usuario']
    search_fields = ['usuario__email', 'horario__cancha__nombre']

admin.site.register(Reserva, ReservaAdmin)