from django.urls import path, include
from rest_framework import routers
from . import views

# Versionado de la API
router = routers.DefaultRouter()
router.register(r'canchas', views.CanchaViewSet)

urlpatterns = [
    # Rutas relacionadas con la API REST
    path('api/v1/', include(router.urls)),
    
]