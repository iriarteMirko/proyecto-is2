from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from apps.horario.models import Horario

class Reserva(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservas')
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE, related_name='reservas')
    hora_reserva_inicio = models.TimeField()  # Hora de inicio de la reserva
    hora_reserva_fin = models.TimeField()  # Hora de fin de la reserva
    fecha_reserva = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
    
    def __str__(self):
        return f'{self.usuario} reserva {self.horario.cancha.nombre} el {self.horario.dia} de {self.hora_reserva_inicio} a {self.hora_reserva_fin}'
    
    def clean(self):
        # Validación: La reserva debe estar dentro del horario disponible
        if not (self.hora_reserva_inicio >= self.horario.hora_inicio and self.hora_reserva_fin <= self.horario.hora_fin):
            raise ValidationError("La reserva debe estar dentro del horario disponible.")
        
        # Validación: La hora reserva de inicio debe ser antes de la hora reserva de fin
        if self.hora_reserva_inicio >= self.hora_reserva_fin:
            raise ValidationError("La hora reserva de inicio debe ser anterior a la hora reserva de fin.")
        
        # Validación: Evitar reservas cruzadas en el mismo horario
        reservas_conflictivas = Reserva.objects.filter(
            horario__cancha=self.horario.cancha,
            horario__dia=self.horario.dia,
            hora_reserva_inicio__lt=self.hora_reserva_fin,
            hora_reserva_fin__gt=self.hora_reserva_inicio
        ).exclude(id=self.id)
        
        if reservas_conflictivas.exists():
            raise ValidationError("El horario seleccionado ya está reservado. Elige otro horario.")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)