from rest_framework import serializers
from .models import Cancha

class CanchaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cancha
        fields = ['id', 'nombre', 'ubicacion', 'disponibilidad', 'responsable', 'fecha_creacion', 'ultima_modificacion']
        read_only_fields = ['responsable', 'fecha_creacion', 'ultima_modificacion']