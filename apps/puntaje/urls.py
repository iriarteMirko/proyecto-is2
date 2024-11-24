from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'puntajes', views.PuntajeViewSet)

urlpatterns = [
    # Rutas de la API REST
    path('api/', include(router.urls)),
    path('calificar/<int:cancha_id>/', views.calificar_cancha, name='calificar_cancha'),
]
