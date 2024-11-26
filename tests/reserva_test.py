from django.test import TestCase
from tests.factories import UsuarioFactory, HorarioFactory, ReservaFactory


class ReservaModelTest(TestCase):
    def setUp(self):
        self.usuario = UsuarioFactory()
        self.horario = HorarioFactory()
        self.reserva = ReservaFactory(usuario=self.usuario, horario=self.horario)
    
    def test_reserva_creacion(self):
        """Verifica que una reserva se crea correctamente"""
        self.assertEqual(self.reserva.usuario, self.usuario)
        self.assertEqual(self.reserva.horario, self.horario)
    
    def test_reserva_valida(self):
        """Verifica que la reserva cumple las validaciones"""
        self.reserva.clean()
        self.assertTrue(True)  # Si no lanza excepción, es válida