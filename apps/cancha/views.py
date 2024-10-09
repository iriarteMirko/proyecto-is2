from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializer import CanchaSerializer
from .models import Cancha

class CanchaViewSet(viewsets.ModelViewSet):
    serializer_class = CanchaSerializer
    queryset = Cancha.objects.all()
    permission_classes = [IsAuthenticated]  # Asegura que solo los usuarios autenticados puedan usar la API
    lookup_field = 'slug'

    def perform_create(self, serializer):
        serializer.save(responsable=self.request.user)
