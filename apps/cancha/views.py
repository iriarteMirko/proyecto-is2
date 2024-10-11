from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.usuario.factories import CanchaConcreteFactory
from .serializer import CanchaSerializer
from .models import Cancha

class CanchaViewSet(viewsets.ModelViewSet):
    serializer_class = CanchaSerializer
    queryset = Cancha.objects.all()
    permission_classes = [IsAuthenticated]  # Asegura que solo los usuarios autenticados puedan usar la API
    lookup_field = 'slug'
    
    def perform_create(self, serializer):
        serializer.save(responsable=self.request.user)

@login_required
def registro_cancha(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        ubicacion = request.POST.get('ubicacion')
        
        # Usar la fábrica para crear la cancha
        cancha_factory = CanchaConcreteFactory()
        cancha = cancha_factory.create_cancha(
            nombre=nombre,
            ubicacion=ubicacion,
            usuario=request.user
        )
        
        if cancha:
            return redirect('inicio')
        else:
            return render(request, 'cancha/registro_cancha.html', {'error': 'Error al crear la cancha. Intente nuevamente.'})
    
    return render(request, 'cancha/registro_cancha.html')