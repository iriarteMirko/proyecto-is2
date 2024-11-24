from django import forms
from .models import Reseña

class ReseñaForm(forms.ModelForm):
    class Meta:
        model = Reseña
        fields = ['calificacion', 'comentario']
        widgets = {
            'calificacion': forms.RadioSelect(choices=[(i, f'{i} Estrella{"s" if i > 1 else ""}') for i in range(1, 6)]),
            'comentario': forms.Textarea(attrs={'placeholder': 'Agrega un comentario opcional...', 'rows': 4}),
        }
        labels = {
            'calificacion': 'Calificación',
            'comentario': 'Comentario',
        }