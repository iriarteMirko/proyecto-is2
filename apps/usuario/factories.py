import logging
from abc import ABC, abstractmethod
from apps.cancha.models import Cancha
from apps.usuario.models import Usuario
from django.contrib.auth.models import Group

logger = logging.getLogger(__name__)

class CanchaFactory(ABC):
    @abstractmethod
    def create_cancha(self, nombre, ubicacion, usuario):
        pass

class CanchaConcreteFactory(CanchaFactory):
    def create_cancha(self, nombre, ubicacion, usuario):
        try:
            cancha = Cancha.objects.create(nombre=nombre, ubicacion=ubicacion, responsable=usuario)
            self._asignar_grupo_responsable(usuario)
            return cancha
        except Exception as e:
            logger.error(f"Error al crear la cancha: {str(e)}")
            return None
    
    # Separar la lógica de asignación de grupos en un método privado (princio SOLID: Single Responsibility)
    def _asignar_grupo_responsable(self, usuario: Usuario):
        cliente_group = Group.objects.get(name='Cliente')
        responsable_group, _ = Group.objects.get_or_create(name='Responsable')
        
        if cliente_group in usuario.groups.all():
            usuario.groups.remove(cliente_group)
            usuario.groups.add(responsable_group)