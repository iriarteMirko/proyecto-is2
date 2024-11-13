from rest_framework import serializers
from .models import Reserva
from apps.horario.serializer import HorarioSerializer
from apps.usuario.serializer import UsuarioSerializer

class ReservaSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    horario = HorarioSerializer(read_only=True)
    cancha_nombre = serializers.CharField(source='horario.cancha.nombre', read_only=True)
    fecha = serializers.DateField(source='horario.fecha', read_only=True)
    hora_inicio = serializers.TimeField(source='horario.hora_inicio', read_only=True)
    hora_fin = serializers.TimeField(source='horario.hora_fin', read_only=True)
    
    class Meta:
        model = Reserva
        fields = ['id', 'usuario', 'horario', 'fecha_reserva', 'cancha_nombre', 'fecha', 'hora_inicio', 'hora_fin']