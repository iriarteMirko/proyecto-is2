from django.shortcuts import render

class VistaBase:
    def procesar_solicitud(self, request, *args, **kwargs):
        """
        Método que será sobrescrito o extendido por las vistas concretas.
        """
        pass

class ResponsableDecorator(VistaBase):
    def __init__(self, vista_envuelta):
        """
        El decorador recibe una instancia de una vista concreta.
        """
        self.vista_envuelta = vista_envuelta
        
    def procesar_solicitud(self, request, *args, **kwargs):
        """
        Verifica si el usuario tiene permisos de 'Responsable'. Si no los tiene, retorna un 404.
        Si los tiene, continúa con la ejecución de la vista.
        """
        if not request.user.is_responsible:  # Utiliza la propiedad del modelo Usuario
            return render(request, 'base/404.html', status=404)
        # Si es responsable, se delega la solicitud a la vista original
        return self.vista_envuelta.procesar_solicitud(request, *args, **kwargs)
