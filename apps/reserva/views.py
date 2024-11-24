from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializer import ReservaSerializer
from apps.horario.models import Horario
from .models import Reserva
from datetime import timedelta, datetime, time
from itertools import groupby
from operator import attrgetter

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

def obtener_dias_horarios_reserva(reserva):
    horarios = Horario.objects.filter(cancha=reserva.horario.cancha).order_by('dia', 'hora_inicio')
    today = datetime.now().date()
    
    dias_horarios = []
    for dia, horarios_dia in groupby(horarios, key=attrgetter('dia')):
        horarios_dia = list(horarios_dia)
        horas_dia = []
        for h in range(24):
            hora_inicio = time(hour=h, minute=0)
            if h == 23:
                hora_fin = time(hour=23, minute=59)
            else:
                hora_fin = (datetime.combine(today, hora_inicio) + timedelta(hours=1)).time()
            
            # Verificar si el bloque coincide con un horario creado
            horario_encontrado = next(
                (horario for horario in horarios_dia if horario.hora_inicio <= hora_inicio < horario.hora_fin),
                None
            )
            if horario_encontrado:
                # Verificar si está reservado
                reservado = Reserva.objects.filter(
                    horario=horario_encontrado,
                    hora_reserva_inicio=hora_inicio,
                    hora_reserva_fin=hora_fin
                )
                if reservado:
                    estado = "rojo"  # Reservado
                else:
                    estado = "verde"  # Disponible
            else:
                estado = "gris"  # Sin horario
            
            horas_dia.append({
                "id": horario_encontrado.id if horario_encontrado else None,
                "hora_inicio": hora_inicio.strftime('%H:%M'),
                "hora_fin": hora_fin.strftime('%H:%M'),
                "estado": estado,
            })
        
        dias_horarios.append({
            "dia": dia.strftime('%Y-%m-%d'),
            "horas": horas_dia,
            "hora_inicio": horarios_dia[0].hora_inicio.strftime('%H:%M') if horarios_dia else None,
            "hora_fin": horarios_dia[-1].hora_fin.strftime('%H:%M') if horarios_dia else None,
        })
    return dias_horarios

@never_cache
@login_required
def detalle_reserva(request, reserva_id):
    try:
        reserva = Reserva.objects.select_related('horario__cancha').get(id=reserva_id, usuario=request.user)
        dias_horarios = obtener_dias_horarios_reserva(reserva)
        print(dias_horarios)
    except Reserva.DoesNotExist:
        messages.error(request, "La reserva que intentas ver ya no existe.")
        return redirect('mis_reservas')
    
    contexto = {
        'reserva': reserva,
        'dias_horarios': dias_horarios,
    }
    return render(request, 'reserva/detalle_reserva.html', contexto)

@never_cache
@login_required
@require_POST
def editar_reserva(request, reserva_id, nuevo_horario_id):
    try:
        reserva = get_object_or_404(Reserva, id=reserva_id, usuario=request.user)
        nuevo_horario = get_object_or_404(Horario, id=nuevo_horario_id, cancha=reserva.horario.cancha)
        
        # Validar que el nuevo horario no esté reservado
        reservado = Reserva.objects.filter(
            horario=nuevo_horario,
            hora_reserva_inicio=nuevo_horario.hora_inicio,
            hora_reserva_fin=nuevo_horario.hora_fin
        ).exclude(id=reserva.id).exists()
        if reservado:
            messages.error(request, "El horario seleccionado ya está reservado.")
            return redirect('detalle_reserva', reserva_id=reserva.id)
        
        # Actualizar la reserva
        reserva.horario = nuevo_horario
        reserva.hora_reserva_inicio = nuevo_horario.hora_inicio
        reserva.hora_reserva_fin = nuevo_horario.hora_fin
        reserva.save()
        
        messages.success(request, "La reserva se actualizó correctamente.")
        return redirect('detalle_reserva', reserva_id=reserva.id)
    except Exception as e:
        messages.error(request, f"Ocurrió un error: {e}")
        return redirect('detalle_reserva', reserva_id=reserva.id)

@never_cache
@login_required
@require_POST
def cancelar_reserva(request, reserva_id):
    try:
        reserva = Reserva.objects.get(id=reserva_id, usuario=request.user)
    except Reserva.DoesNotExist:
        messages.error(request, "La reserva que intentas ver ya no existe.")
        return redirect('mis_reservas')
    
    reserva.delete()
    messages.success(request, "Reserva cancelada exitosamente.")
    return HttpResponseRedirect(reverse('mis_reservas'))