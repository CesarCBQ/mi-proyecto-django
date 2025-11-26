# libros/views.py

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import CreateView # <-- Importación necesaria para AutorCreateView
from django.urls import reverse_lazy # <-- Importación necesaria para success_url

from .models import Libro, Autor # Modelos
from .forms import AutorForm # <-- ¡CRÍTICO! Necesita importar el formulario

# Opcional: Si el archivo existe, descoméntalo
# from usuarios.forms import ReseñaForm 

# VISTA GENÉRICA (ListView) - Listado de Libros
class LibroListView(ListView):
    model = Libro
    template_name = 'libros/lista_libros.html'
    context_object_name = 'libros'
    paginate_by = 10 

# VISTA FUNCIONAL - Detalle de Libro (Ruta Dinámica)
def detalle_libro(request, slug):
    libro = get_object_or_404(Libro, slug=slug) 
    
    context = {
        'libro': libro,
        # ... (dejar reseña y form_resena comentados por ahora)
    }
    
    return render(request, 'libros/detalle_libro.html', context)

# 🚀 VISTA GENÉRICA (CreateView) - Crear Autor (AGREGADA)
class AutorCreateView(CreateView):
    """Permite crear un nuevo autor usando AutorForm."""
    model = Autor
    form_class = AutorForm # Usa el formulario que definiste en libros/forms.py
    template_name = 'libros/crear_autor.html'
    # Redirige a la lista de libros después de guardar
    success_url = reverse_lazy('lista_libros')