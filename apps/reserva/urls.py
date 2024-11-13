from django.urls import path
from . import views

urlpatterns = [
    path('reservar/<int:horario_id>/', views.realizar_reserva, name='realizar_reserva'),
]
