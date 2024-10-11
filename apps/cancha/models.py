from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth.models import Group

class Cancha(models.Model):
    nombre = models.CharField('Nombre de la cancha', max_length=100, blank=False, null=False)
    ubicacion = models.CharField('Ubicación', max_length=255, blank=False, null=False)
    disponibilidad = models.BooleanField('Disponible', default=False, blank=False, null=False)
    fecha_creacion = models.DateField(auto_now_add=True)
    ultima_modificacion = models.DateField(auto_now=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    
    # Relación con el usuario responsable
    responsable = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='canchas')
    
    class Meta:
        verbose_name = 'Cancha'
        verbose_name_plural = 'Canchas'
    
    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        # Verificar si el usuario pertenece al grupo 'Responsable'
        if not self.responsable.groups.filter(name='Responsable').exists():
            cliente_group = Group.objects.get(name='Cliente')
            responsable_group, created = Group.objects.get_or_create(name='Responsable')
            
            # Remover del grupo Cliente y agregar a Responsable
            self.responsable.groups.remove(cliente_group)
            self.responsable.groups.add(responsable_group)
        
        # Generar el slug basado en el nombre si no está definido
        if not self.slug:
            self.slug = slugify(self.nombre)
        
        super(Cancha, self).save(*args, **kwargs)