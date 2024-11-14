from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializer import HorarioSerializer
from .models import Horario
from apps.cancha.models import Cancha

# ViewSet para la API REST
class HorarioViewSet(viewsets.ModelViewSet):
    serializer_class = HorarioSerializer
    queryset = Horario.objects.all()
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        dia = request.data.get('dia')
        hora_inicio = request.data.get('hora_inicio')
        cancha_id = request.data.get('cancha')
        # Verificar si ya existe un horario para el día y la cancha
        if Horario.objects.filter(cancha_id=cancha_id, dia=dia).exists():
            return Response(
                {"detail": "Ya existe un horario para este día y cancha."},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Crear instancia de Horario para validación
        horario = Horario(
            dia=dia,
            hora_inicio=hora_inicio,
            hora_fin=request.data.get('hora_fin'),
            cancha_id=cancha_id
        )
        try:
            horario.clean()
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return super(HorarioViewSet, self).create(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        return super(HorarioViewSet, self).destroy(request, *args, **kwargs)

@login_required
def configurar_horarios(request, cancha_id):
    cancha = get_object_or_404(Cancha, id=cancha_id, responsable=request.user)
    if request.method == 'POST':
        # Procesar el formulario para crear horarios según el rango de horas y días seleccionados
        # Código para crear horarios...
        messages.success(request, 'Horarios configurados exitosamente.')
        return redirect('detalle_cancha', cancha_id=cancha.id, cancha_slug=cancha.slug)
    horarios = cancha.horarios.all()
    return render(request, 'horario/configurar_horarios.html', {'cancha': cancha, 'horarios': horarios})