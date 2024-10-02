from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.usuario.urls')),
    path('usuario/', include('apps.usuario.urls')),
    path('', include('apps.cliente.urls')),
    path('cliente/', include('apps.cliente.urls')),
    path('', include('apps.responsable.urls')),
    path('responsable/', include('apps.responsable.urls')),
    path('', include('apps.cancha.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Configuración de la vista personalizada para errores 404
handler404 = 'apps.usuario.views.error_404_view'