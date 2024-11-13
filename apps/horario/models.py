from django.db import models
from apps.cancha.models import Cancha

class Horario(models.Model):
    cancha = models.ForeignKey(Cancha, on_delete=models.CASCADE, related_name='horarios')
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    disponible = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Horario'
        verbose_name_plural = 'Horarios'
        unique_together = ('cancha', 'fecha', 'hora_inicio')
    
    def __str__(self):
        return f"{self.cancha.nombre} - {self.fecha} {self.hora_inicio}-{self.hora_fin}"