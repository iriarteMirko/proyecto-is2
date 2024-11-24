from rest_framework import serializers
from .models import Puntaje

class PuntajeSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField(read_only=True)
    cancha = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Puntaje
        fields = ['id', 'usuario', 'cancha', 'calificacion', 'comentario', 'fecha_creacion']
        read_only_fields = ['id', 'usuario', 'cancha', 'fecha_creacion']
    
    def validate_puntaje(self, value):
        """Validar que el puntaje esté entre 1 y 5"""
        if value < 1 or value > 5:
            raise serializers.ValidationError("El puntaje debe estar entre 1 y 5.")
        return value