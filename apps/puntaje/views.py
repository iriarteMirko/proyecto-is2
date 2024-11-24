from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializer import PuntajeSerializer
from .models import Puntaje
from .forms import PuntajeForm
from apps.cancha.models import Cancha

class PuntajeViewSet(viewsets.ModelViewSet):
    serializer_class = PuntajeSerializer
    queryset = Puntaje.objects.all()
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(responsable=self.request.user)

@login_required
def calificar_cancha(request, cancha_id):
    cancha = get_object_or_404(Cancha, id=cancha_id)
    
    # Verificar si el usuario ya calificó esta cancha
    if Puntaje.objects.filter(usuario=request.user, cancha=cancha).exists():
        messages.error(request, "Ya calificaste esta cancha.")
        return redirect('detalle_cancha', cancha_id=cancha.id, cancha_slug=cancha.slug)
    
    if request.method == 'POST':
        form = PuntajeForm(request.POST)
        if form.is_valid():
            puntaje = form.save(commit=False)
            puntaje.usuario = request.user
            puntaje.cancha = cancha
            puntaje.save()
            messages.success(request, "Gracias por calificar la cancha.")
            return redirect('detalle_cancha', cancha_id=cancha.id, cancha_slug=cancha.slug)
    else:
        form = PuntajeForm()
    
    return render(request, 'puntaje/calificar_cancha.html', {'form': form, 'cancha': cancha})