from rest_framework import serializers
from .models import Cancha

class CanchaSerializer(serializers.ModelSerializer):
    responsable_nombre = serializers.ReadOnlyField(source='responsable.get_full_name')
    
    class Meta:
        model = Cancha
        fields = ['id', 'nombre', 'ubicacion', 'disponibilidad', 'responsable', 'responsable_nombre', 'fecha_creacion', 'ultima_modificacion']
        read_only_fields = ['responsable', 'fecha_creacion', 'ultima_modificacion']  # Los campos de solo lectura