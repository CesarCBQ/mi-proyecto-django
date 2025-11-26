# usuarios/forms.py

from django import forms
from .models import Reseña

class ReseñaForm(forms.ModelForm):
    # Opcional: Personalizar las etiquetas o campos
    rating = forms.IntegerField(
        label='Puntuación',
        widget=forms.Select(choices=[(i, str(i)) for i in range(1, 6)]),
        min_value=1, max_value=5
    )
    
    class Meta:
        model = Reseña
        # Solo necesitamos que el usuario llene el rating y el contenido. 
        # Los campos 'usuario' y 'libro' los llenaremos en la vista.
        fields = ['rating', 'contenido'] 
        widgets = {
            'contenido': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }