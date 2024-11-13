from rest_framework import serializers
from .models import Reserva
from apps.horario.models import Horario

class ReservaSerializer(serializers.ModelSerializer):
    usuario = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Reserva
        fields = ['id', 'usuario', 'horario', 'hora_reserva_inicio', 'hora_reserva_fin', 'fecha_reserva']
    
    def validate(self, data):
        horario = data['horario']
        
        # Validar que la reserva esté dentro del horario de disponibilidad
        if not (data['hora_reserva_inicio'] >= horario.hora_inicio and data['hora_reserva_fin'] <= horario.hora_fin):
            raise serializers.ValidationError("La reserva debe estar dentro del horario disponible.")
        
        # Verificar conflicto con otras reservas
        reservas_conflictivas = Reserva.objects.filter(
            horario__cancha=horario.cancha,
            horario__dia=horario.dia,
            hora_reserva_inicio__lt=data['hora_reserva_fin'],
            hora_reserva_fin__gt=data['hora_reserva_inicio']
        ).exclude(usuario=data['usuario'])
        
        if reservas_conflictivas.exists():
            raise serializers.ValidationError("El horario seleccionado ya está reservado. Elige otro horario.")
        
        return data