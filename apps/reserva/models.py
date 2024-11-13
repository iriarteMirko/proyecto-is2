from django.db import models
from apps.horario.models import Horario
from apps.usuario.models import Usuario

class Reserva(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='reservas')
    horario = models.OneToOneField(Horario, on_delete=models.CASCADE, related_name='reserva')
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
    
    def __str__(self):
        return f"{self.usuario} - {self.horario}"