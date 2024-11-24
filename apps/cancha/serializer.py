from rest_framework import serializers
from .models import Cancha

class CanchaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cancha
        fields = ['id', 'nombre', 'fecha_creacion', 'ultima_modificacion', 'responsable', 'imagen', 'slug']
        read_only_fields = ['fecha_creacion', 'ultima_modificacion', 'slug']