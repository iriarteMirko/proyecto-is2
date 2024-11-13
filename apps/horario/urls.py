from django.urls import path
from . import views

urlpatterns = [
    path('configurar/<int:cancha_id>/', views.configurar_horarios, name='configurar_horarios'),
]
