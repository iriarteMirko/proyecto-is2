import factory
from datetime import time, timedelta
from django.utils.timezone import now
from django.contrib.auth.models import Group
from apps.usuario.models import Usuario
from apps.cancha.models import Cancha
from apps.direccion.models import Direccion
from apps.horario.models import Horario
from apps.reseña.models import Reseña
from apps.reserva.models import Reserva


# Usuario Factory
class UsuarioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Usuario
        skip_postgeneration_save = True
    
    email = "user@test.com"
    dni = factory.Faker("random_number", digits=8, fix_len=True)
    nombre = "test"
    apellidos = "user"
    celular = factory.Faker("random_number", digits=9, fix_len=True) 
    password = factory.PostGenerationMethodCall("set_password", "TestPassword123")
    
    @factory.post_generation
    def add_group(self, create, extracted, **kwargs):
        if not create:
            return
        cliente_group, _ = Group.objects.get_or_create(name="Cliente")
        self.groups.add(cliente_group)


# Cancha Factory
class CanchaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cancha
        skip_postgeneration_save = True
    
    responsable = factory.SubFactory(UsuarioFactory)
    nombre = "Cancha Test"
    disponibilidad = False
    imagen = None


# Dirección Factory
class DireccionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Direccion
    
    cancha = factory.SubFactory(CanchaFactory)
    tipo_calle = "Avenida"
    nombre_calle = factory.Faker("street_name")
    numero_calle = factory.Faker("building_number")
    distrito = "Miraflores"
    referencia = factory.Faker("sentence", nb_words=5)


# Horario Factory
class HorarioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Horario
    
    cancha = factory.SubFactory(CanchaFactory)
    dia = factory.LazyFunction(lambda: now().date() + timedelta(days=1))  # Fecha de mañana
    hora_inicio = time(9, 0)
    hora_fin = time(18, 0)


# Reseña Factory
class ReseñaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Reseña
    
    usuario = factory.SubFactory(UsuarioFactory)
    cancha = factory.SubFactory(CanchaFactory)
    calificacion = factory.Iterator([1, 2, 3, 4, 5])  # Genera calificaciones entre 1 y 5
    comentario = factory.Faker("paragraph", nb_sentences=3)


# Reserva Factory
class ReservaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Reserva
    
    usuario = factory.SubFactory(UsuarioFactory)
    horario = factory.SubFactory(HorarioFactory)
    hora_reserva_inicio = time(10, 0)
    hora_reserva_fin = time(11, 0)
