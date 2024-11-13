from rest_framework import serializers
from .models import Horario
from django.utils import timezone

class HorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horario
        fields = ['id', 'cancha', 'dia', 'hora_inicio', 'hora_fin']
    
    def validate(self, data):
        ahora = timezone.now()
        
        # Validar que el día y la hora sean en el futuro
        if data['dia'] < ahora.date() or (data['dia'] == ahora.date() and data['hora_inicio'] <= ahora.time()):
            raise serializers.ValidationError("El horario debe estar en el futuro.")
        
        # Validar que la hora de inicio sea antes de la hora de fin
        if data['hora_inicio'] >= data['hora_fin']:
            raise serializers.ValidationError("La hora de inicio debe ser anterior a la hora de fin.")
        
        return data