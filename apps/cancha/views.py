from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.usuario.factories import CanchaConcreteFactory
from apps.direccion.models import Direccion
from .serializer import CanchaSerializer
from .models import Cancha

class CanchaViewSet(viewsets.ModelViewSet):
    serializer_class = CanchaSerializer
    queryset = Cancha.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'
    
    def perform_create(self, serializer):
        serializer.save(responsable=self.request.user)

@login_required
def registro_cancha(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        tipo_calle = request.POST.get('tipo_calle')
        nombre_calle = request.POST.get('nombre_calle')
        numero_calle = request.POST.get('numero_calle')
        distrito = request.POST.get('distrito')
        referencia = request.POST.get('referencia', '')
        
        # Usar la fábrica para crear la cancha
        cancha_factory = CanchaConcreteFactory()
        cancha = cancha_factory.create_cancha(
            nombre=nombre,
            usuario=request.user
        )
        
        if cancha:
            Direccion.objects.create(
                tipo_calle=tipo_calle,
                nombre_calle=nombre_calle,
                numero_calle=numero_calle,
                distrito=distrito,
                referencia=referencia,
                cancha=cancha
            )
            return redirect('inicio')
        else:
            return render(request, 'cancha/registro_cancha.html', {'error': 'Error al crear la cancha. Intente nuevamente.'})
    
    return render(request, 'cancha/registro_cancha.html')