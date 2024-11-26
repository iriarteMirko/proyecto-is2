from django.test import TestCase
from tests.factories import CanchaFactory, DireccionFactory


class DireccionModelTest(TestCase):
    def setUp(self):
        self.cancha = CanchaFactory()
        self.direccion = DireccionFactory(cancha=self.cancha)
    
    def test_direccion_creacion(self):
        """Verifica que la dirección se crea correctamente"""
        self.assertEqual(self.direccion.cancha, self.cancha)
        self.assertEqual(self.direccion.tipo_calle, "calle")
        self.assertEqual(self.direccion.distrito, "miraflores")