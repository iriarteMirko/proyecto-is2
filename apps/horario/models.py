from django.db import models
from django.utils import timezone
from apps.cancha.models import Cancha

class Horario(models.Model):
    cancha = models.ForeignKey(Cancha, on_delete=models.CASCADE, related_name='horarios')
    dia = models.DateField()  # Día específico para el rango horario
    hora_inicio = models.TimeField()  # Hora de inicio del rango de disponibilidad
    hora_fin = models.TimeField()  # Hora de fin del rango de disponibilidad
    
    class Meta:
        verbose_name = 'Horario'
        verbose_name_plural = 'Horarios'
        unique_together = ['cancha', 'dia']  # Solo un rango horario por día por cancha
    
    def __str__(self):
        return f'{self.cancha.nombre} - {self.dia} de {self.hora_inicio} a {self.hora_fin}'
    
    def save(self, *args, **kwargs):
        ahora = timezone.now()
        
        # Validación: solo permitir horarios en fechas futuras o la fecha actual si es en horas posteriores.
        if self.dia < ahora.date() or (self.dia == ahora.date() and self.hora_inicio <= ahora.time()):
            raise ValueError("El horario debe ser en una fecha y hora futuras.")
        
        # Validación: la hora de inicio debe ser antes de la hora de fin.
        if self.hora_inicio >= self.hora_fin:
            raise ValueError("La hora de inicio debe ser anterior a la hora de fin.")
        
        super().save(*args, **kwargs)