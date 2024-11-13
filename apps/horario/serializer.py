from rest_framework import serializers
from .models import Horario

class HorarioSerializer(serializers.ModelSerializer):
    cancha_nombre = serializers.CharField(source='cancha.nombre', read_only=True)
    
    class Meta:
        model = Horario
        fields = ['id', 'cancha', 'cancha_nombre', 'fecha', 'hora_inicio', 'hora_fin', 'disponible']
        read_only_fields = ['disponible']