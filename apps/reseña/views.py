from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializer import ReseñaSerializer
from .models import Reseña
from apps.cancha.models import Cancha

class ReseñaViewSet(viewsets.ModelViewSet):
    serializer_class = ReseñaSerializer
    queryset = Reseña.objects.all()
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(responsable=self.request.user)

@login_required
def calificar_cancha(request, cancha_id):
    cancha = get_object_or_404(Cancha, id=cancha_id)
    
    # Verificar si el usuario ya calificó esta cancha
    if Reseña.objects.filter(usuario=request.user, cancha=cancha).exists():
        messages.error(request, "Ya calificaste esta cancha.")
        return redirect('detalle_cancha', cancha_id=cancha.id, cancha_slug=cancha.slug)
    
    if request.method == 'POST':
        calificacion = int(request.POST.get('calificacion', 0))
        comentario = request.POST.get('comentario', '')
        
        if calificacion < 1 or calificacion > 5:
            messages.error(request, "La calificación debe estar entre 1 y 5.")
            return redirect('detalle_cancha', cancha_id=cancha.id, cancha_slug=cancha.slug)
        
        # Crear la reseña
        Reseña.objects.create(
            usuario=request.user,
            cancha=cancha,
            calificacion=calificacion,
            comentario=comentario
        )
        messages.success(request, "Gracias por calificar la cancha.")
        return redirect('detalle_cancha', cancha_id=cancha.id, cancha_slug=cancha.slug)
    
    return redirect('detalle_cancha', cancha_id=cancha.id, cancha_slug=cancha.slug)