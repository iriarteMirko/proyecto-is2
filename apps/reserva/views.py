from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializer import ReservaSerializer
from .models import Reserva
from apps.horario.models import Horario

# ViewSet para la API REST
class ReservaViewSet(viewsets.ModelViewSet):
    serializer_class = ReservaSerializer
    queryset = Reserva.objects.all()
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        horario_id = request.data.get('horario')
        hora_reserva_inicio = request.data.get('hora_reserva_inicio')
        hora_reserva_fin = request.data.get('hora_reserva_fin')
        # Crear instancia de Reserva para validación
        reserva = Reserva(
            usuario=request.user,
            horario_id=horario_id,
            hora_reserva_inicio=hora_reserva_inicio,
            hora_reserva_fin=hora_reserva_fin
        )
        try:
            reserva.clean()
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return super(ReservaViewSet, self).create(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        return super(ReservaViewSet, self).destroy(request, *args, **kwargs)

@login_required
def realizar_reserva(request, horario_id):
    horario = get_object_or_404(Horario, id=horario_id, disponible=True)
    if request.method == 'POST':
        Reserva.objects.create(usuario=request.user, horario=horario)
        horario.disponible = False
        horario.save()
        messages.success(request, 'Reserva realizada exitosamente.')
        return redirect('mis_reservas')
    return render(request, 'reserva/confirmar_reserva.html', {'horario': horario})