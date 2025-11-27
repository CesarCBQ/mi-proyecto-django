from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.utils.text import slugify 

# Seguridad
from django.contrib.auth.mixins import UserPassesTestMixin


from .models import Categoria, Libro, Autor
# 🚨 MANTENEMOS COMENTADA LA IMPORTACIÓN DE FORMS, COMO SOLICITASTE
# from .forms import AutorForm, CategoriaForm, LibroForm 


# ----------------------------------------------------------------------
# --- MIXIN DE SEGURIDAD PARA ADMINISTRACIÓN ---
# ----------------------------------------------------------------------
class SuperuserRequiredMixin(UserPassesTestMixin):
    """Asegura que solo el superusuario puede acceder a la vista."""
    def test_func(self):
        return self.request.user.is_superuser

# ----------------------------------------------------------------------
# --- VISTAS LECTURA ---
# ----------------------------------------------------------------------
class LibroListView(ListView):
    model = Libro
    template_name = 'libros/home.html' 
    context_object_name = 'libros'
    paginate_by = 10 
    # 🌟 CORRECCIÓN APLICADA: Cambiar el orden a 'pk' (Primary Key) 
    # para asegurar que los libros 1 a 10 aparezcan primero, 
    # satisfaciendo el test de paginación.
    ordering = ['pk'] 

# VISTA FUNCIONAL - Detalle de Libro (Ruta Dinámica)
def detalle_libro(request, slug):
    """Muestra la información detallada de un libro."""
    libro = get_object_or_404(Libro, slug=slug) 
    
    context = {
        'libro': libro,
    }
    
    return render(request, 'libros/detalle_libro.html', context)

# 🔑 VISTA FUNCIONAL AÑADIDA - Renderiza la plantilla de login 🔑
def login_page(request):
    """Renderiza la plantilla de inicio de sesión para Firebase Auth."""
    return render(request, 'libros/login.html')

# ----------------------------------------------------------------------
# --- VISTAS ADMINISTRACIÓN (CRUD) ---
# ----------------------------------------------------------------------

# 🚀 VISTA GENÉRICA (CreateView) - Crear Autor
class AutorCreateView(SuperuserRequiredMixin, CreateView):
    model = Autor
    fields = ['nombre', 'biografia', 'fecha_nacimiento'] 
    template_name = 'libros/crear_autor.html' 
    success_url = reverse_lazy('home')

# 🚀 VISTA GENÉRICA (CreateView) - Crear Categoría
class CategoriaCreateView(SuperuserRequiredMixin, CreateView):
    model = Categoria
    fields = ['nombre'] 
    template_name = 'libros/crear_autor.html' 
    success_url = reverse_lazy('home')

# 🚀 VISTA GENÉRICA (CreateView) - Crear Libro
class LibroCreateView(SuperuserRequiredMixin, CreateView):
    model = Libro
    fields = ['titulo', 'isbn', 'fecha_publicacion', 'autor', 'categoria']
    template_name = 'libros/libro_form.html'
    success_url = reverse_lazy('home') 

    # 🟢 MÉTODO AGREGADO PARA PREVENIR EL NoReverseMatch 🟢
    def form_valid(self, form):
        self.object = form.save(commit=False)
        if not self.object.slug:
            self.object.slug = slugify(self.object.titulo)
        self.object.save()
        return super().form_valid(form)

# 🚀 VISTA GENÉRICA (UpdateView) - Editar Libro
class LibroUpdateView(SuperuserRequiredMixin, UpdateView):
    model = Libro
    fields = ['titulo', 'isbn', 'fecha_publicacion', 'autor', 'categoria']
    template_name = 'libros/libro_form.html'
    
    def get_success_url(self):
        # 🟢 CORRECCIÓN PREVIA: Usamos el namespace para el reverso.
        return reverse_lazy('libros:detalle_libro', kwargs={'slug': self.object.slug})

# 🚀 VISTA GENÉRICA (DeleteView) - Eliminar Libro
class LibroDeleteView(SuperuserRequiredMixin, DeleteView):
    model = Libro
    template_name = 'libros/libro_confirm_delete.html' 
    success_url = reverse_lazy('home')