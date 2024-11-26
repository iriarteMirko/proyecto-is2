from django.test import TestCase
from django.contrib.auth.models import Group
from tests.factories import UsuarioFactory, CanchaFactory


class CanchaModelTest(TestCase):
    def setUp(self):
        self.responsable = UsuarioFactory()
        self.cancha = CanchaFactory(responsable=self.responsable)
        responsable_group, _ = Group.objects.get_or_create(name="Responsable")
        self.responsable.groups.add(responsable_group)
    
    def test_cancha_creacion(self):
        """Verifica que una cancha se crea correctamente"""
        self.assertEqual(self.cancha.nombre, "Cancha Test")
        self.assertEqual(self.cancha.responsable, self.responsable)
    
    def test_cancha_disponibilidad(self):
        """Verifica que la disponibilidad por defecto es False"""
        self.assertFalse(self.cancha.disponibilidad)