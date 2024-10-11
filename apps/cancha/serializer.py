from rest_framework import serializers
from .models import Cancha
from apps.direccion.models import Direccion

class DireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direccion
        fields = ['tipo_calle', 'nombre_calle', 'numero_calle', 'distrito', 'referencia']

class CanchaSerializer(serializers.ModelSerializer):
    direccion = DireccionSerializer(read_only=True)
    
    class Meta:
        model = Cancha
        fields = ['id', 'nombre', 'disponibilidad', 'responsable', 'fecha_creacion', 'ultima_modificacion', 'direccion']
        read_only_fields = ['responsable', 'fecha_creacion', 'ultima_modificacion']