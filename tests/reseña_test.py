from django.test import TestCase
from tests.factories import UsuarioFactory, CanchaFactory, ReseñaFactory


class ReseñaModelTest(TestCase):
    def setUp(self):
        self.usuario = UsuarioFactory()
        self.cancha = CanchaFactory()
        self.reseña = ReseñaFactory(usuario=self.usuario, cancha=self.cancha)
    
    def test_reseña_creacion(self):
        """Verifica que una reseña se crea correctamente"""
        self.assertEqual(self.reseña.usuario, self.usuario)
        self.assertEqual(self.reseña.cancha, self.cancha)
        self.assertEqual(self.reseña.calificacion, 5)
    
    def test_reseña_unica(self):
        """Verifica que no se puede crear una reseña duplicada"""
        with self.assertRaises(Exception):
            ReseñaFactory(usuario=self.usuario, cancha=self.cancha)