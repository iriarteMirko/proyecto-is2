from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializer import CanchaSerializer
from apps.usuario.factory import CanchaConcreteFactory
from apps.horario.models import Horario
from apps.reserva.models import Reserva
from .models import Cancha
from datetime import date, timedelta, datetime
import re

class CanchaViewSet(viewsets.ModelViewSet):
    serializer_class = CanchaSerializer
    queryset = Cancha.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'
    
    def perform_create(self, serializer):
        serializer.save(responsable=self.request.user)

def obtener_dias_horarios(cancha):
    today = date.today()
    start_date = today.replace(day=1)
    end_date = (start_date + timedelta(days=31)).replace(day=1) - timedelta(days=1)
    
    horarios = Horario.objects.filter(cancha=cancha, dia__range=(start_date, end_date))
    dias_horarios = []
    
    for horario in horarios:
        reservas = Reserva.objects.filter(horario=horario)
        horarios_disponibles = []
        
        # Solo añadimos el horario disponible si no está reservado
        for i in range(horario.hora_inicio.hour, horario.hora_fin.hour):
            hora_inicio = horario.hora_inicio.replace(hour=i, minute=0, second=0)
            hora_inicio_datetime = datetime.combine(horario.dia, hora_inicio)
            hora_fin = (hora_inicio_datetime + timedelta(hours=1)).time()
            
            if not reservas.filter(hora_reserva_inicio=hora_inicio, hora_reserva_fin=hora_fin).exists():
                horarios_disponibles.append({
                    "hora_inicio": hora_inicio.strftime("%H:%M"),
                    "hora_fin": hora_fin.strftime("%H:%M"),
                })
        
        # Agrega solo los días que tienen horarios disponibles
        if horarios_disponibles:
            dias_horarios.append({
                "dia": horario.dia.strftime("%Y-%m-%d"),
                "horarios": horarios_disponibles,
            })
    
    return dias_horarios

@login_required
def detalle_cancha(request, cancha_id, cancha_slug):
    cancha = get_object_or_404(Cancha, id=cancha_id, slug=cancha_slug)
    responsable = request.user == cancha.responsable
    dias_horarios = obtener_dias_horarios(cancha)
    
    contexto = {
        'cancha': cancha,
        'responsable': responsable,
        'dias_horarios': dias_horarios
    }
    return render(request, 'cancha/detalle_cancha/detalle_cancha.html', contexto)

def validar_datos_cancha(request):
    nombre = request.POST.get('nombre', '').strip()
    tipo_calle = request.POST.get('tipo_calle', '').strip()
    nombre_calle = request.POST.get('nombre_calle', '').strip()
    numero_calle = request.POST.get('numero_calle', '').strip()
    distrito = request.POST.get('distrito', '').strip()
    referencia = request.POST.get('referencia', '').strip()
    imagen = request.FILES.get('imagen')
    
    if not all([nombre, tipo_calle, nombre_calle, numero_calle, distrito]):
        return None, 'Todos los campos obligatorios deben estar completos.'
    if not re.match(r'^[A-Za-z0-9\s]+$', nombre):
        return None, 'El nombre solo puede contener letras, números y espacios.'
    if not numero_calle.isdigit():
        return None, 'El número de la calle debe ser un valor numérico.'
    if referencia and not re.match(r'^[A-Za-z0-9\s,.]+$', referencia):
        return None, 'La referencia solo puede contener letras, números, comas y puntos.'
    if not imagen:
        imagen = 'canchas/default-cancha.jpg'
    
    return {
        'nombre': nombre,
        'tipo_calle': tipo_calle,
        'nombre_calle': nombre_calle,
        'numero_calle': numero_calle,
        'distrito': distrito,
        'referencia': referencia,
        'imagen': imagen
    }, None

@login_required
def registro_cancha(request):
    if request.method == 'POST':
        datos, error = validar_datos_cancha(request)
        if error:
            return render(request, 'cancha/registro_cancha.html', {'error': error})
        
        # Usar la fábrica para crear la cancha con su dirección
        factory = CanchaConcreteFactory()
        cancha = factory.create_cancha(
            nombre=datos['nombre'],
            usuario=request.user
        )
        if cancha:
            direccion = factory.create_direccion(
                cancha=cancha,
                tipo_calle=datos['tipo_calle'],
                nombre_calle=datos['nombre_calle'],
                numero_calle=datos['numero_calle'],
                distrito=datos['distrito'],
                referencia=datos['referencia'],
            )
            if direccion:
                messages.success(request, 'Cancha registrada correctamente.')
                return redirect('detalle_cancha', cancha.id, cancha.slug)
            else:
                return render(request, 'cancha/registro_cancha.html', {'error': 'Error al registrar la dirección. Intente nuevamente.'})
        return render(request, 'cancha/registro_cancha.html', {'error': 'Error al crear la cancha. Intente nuevamente.'})
    return render(request, 'cancha/registro_cancha.html')

@login_required
def editar_cancha(request, cancha_id, cancha_slug):
    cancha = get_object_or_404(Cancha, id=cancha_id, slug=cancha_slug, responsable=request.user)
    direccion = cancha.direcciones.first()
    if request.method == 'POST':
        datos, error = validar_datos_cancha(request)
        if error:
            messages.error(request, error)
            return render(request, 'cancha/editar_cancha/editar_cancha.html', {'cancha': cancha})
        if not direccion:
            messages.error(request, 'Dirección no encontrada.')
            return render(request, 'cancha/editar_cancha/editar_cancha.html', {'cancha': cancha})
        
        cancha.nombre = datos['nombre']
        cancha.imagen = datos['imagen']
        direccion.tipo_calle = datos['tipo_calle']
        direccion.nombre_calle = datos['nombre_calle']
        direccion.numero_calle = datos['numero_calle']
        direccion.distrito = datos['distrito']
        direccion.referencia = datos['referencia']
        
        direccion.save()
        cancha.save()
        
        messages.success(request, 'Datos actualizados correctamente.')
        return redirect('detalle_cancha', cancha.id, cancha.slug)
    return render(request, 'cancha/editar_cancha/editar_cancha.html', {'cancha': cancha})

@login_required
@require_POST
def cambiar_imagen(request):
    user = request.user
    if request.method == 'POST':
        imagen = request.FILES.get('imagen')
        if imagen:
            user.imagen = imagen
            user.save()
            messages.success(request, 'Imagen actualizada correctamente.')
            return redirect('perfil', user.id, user.slug)
        else:
            user.imagen = 'usuarios/default-avatar.jpg'
            user.save()
            return redirect('perfil', user.id, user.slug)
    return render(request, 'usuario/editar_perfil/editar_perfil.html', {'user': user})

@login_required
@require_POST
def eliminar_cancha(request, cancha_id, cancha_slug):
    cancha = get_object_or_404(Cancha, id=cancha_id, slug=cancha_slug, responsable=request.user)
    if request.method == 'POST':
        contraseña = request.POST.get('password')
        if not request.user.check_password(contraseña):
            messages.error(request, 'Contraseña incorrecta.')
            return redirect('editar_cancha', cancha_id, cancha_slug)
        cancha.delete()
        messages.success(request, 'La cancha fue eliminada correctamente.')
        return redirect('inicio')

