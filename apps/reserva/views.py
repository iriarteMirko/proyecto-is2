from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Reserva
from apps.horario.models import Horario

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