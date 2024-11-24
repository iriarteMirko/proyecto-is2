from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'reservas', views.ReservaViewSet)

urlpatterns = [
    # Rutas relacionadas con la API REST
    path('api/', include(router.urls)),
    path('detalle_reserva/<int:reserva_id>/', views.detalle_reserva, name='detalle_reserva'),
    path('detalle_reserva/<int:reserva_id>/cancelar/', views.cancelar_reserva, name='cancelar_reserva'),
    path('editar-reserva/<int:reserva_id>/<int:nuevo_horario_id>/', views.editar_reserva, name='editar_reserva'),
]