from django.test import TestCase
from tests.factories import CanchaFactory, HorarioFactory


class HorarioModelTest(TestCase):
    def setUp(self):
        self.cancha = CanchaFactory()
        self.horario = HorarioFactory(cancha=self.cancha)
    
    def test_horario_creacion(self):
        """Verifica que un horario se crea correctamente"""
        self.assertEqual(self.horario.cancha, self.cancha)
        self.assertEqual(self.horario.hora_inicio.strftime('%H:%M'), "10:00")
        self.assertEqual(self.horario.hora_fin.strftime('%H:%M'), "12:00")
    
    def test_horario_valido(self):
        """Verifica que el horario cumple las validaciones"""
        self.horario.clean()
        self.assertTrue(True)  # Si no lanza excepción, es válido