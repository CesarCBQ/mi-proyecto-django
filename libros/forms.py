# libros/forms.py

from django import forms
from .models import Autor, Categoria, Libro 

# --- Formulario de Libro (CRÍTICO) ---
class LibroForm(forms.ModelForm):
    """Formulario usado para Crear y Editar libros."""
    class Meta:
        model = Libro
        fields = ['titulo', 'isbn', 'fecha_publicacion', 'autor', 'categoria']
        
        widgets = {
            'fecha_publicacion': forms.DateInput(attrs={'type': 'date'}),
        }


# --- Formularios Corregidos (Autor y Categoría) ---

class AutorForm(forms.ModelForm):
    """Formulario para crear y editar autores."""
    class Meta: 
        model = Autor
        fields = ('nombre',) 

class CategoriaForm(forms.ModelForm):
    """Formulario para crear y editar categorías."""
    class Meta: 
        model = Categoria
        fields = ('nombre',)