from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Horario
from apps.cancha.models import Cancha

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