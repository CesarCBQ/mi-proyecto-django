# libros/forms.py

from django import forms
from .models import Autor # Importa el modelo Autor

class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ['nombre', 'biografia', 'fecha_nacimiento']