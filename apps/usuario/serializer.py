from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField(source='get_full_name')
    
    class Meta:
        model = Usuario
        fields = [
            'id', 'email', 'dni', 'nombre', 'apellidos', 'celular', 'imagen', 
            'is_active', 'slug', 'full_name'
        ]
        read_only_fields = ['is_active', 'slug']  # Algunos campos solo de lectura