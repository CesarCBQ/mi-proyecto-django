from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.utils.text import slugify 

# Seguridad
from django.contrib.auth.mixins import UserPassesTestMixin
# 🟢 IMPORTACIONES PARA FIREBASE AUTH 🟢
from firebase_admin import auth
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json 


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
    template_name = 'libros/lista_libros.html' 
    context_object_name = 'libros'
    paginate_by = 10 

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
    success_url = reverse_lazy('lista_libros')

# 🚀 VISTA GENÉRICA (CreateView) - Crear Categoría
class CategoriaCreateView(SuperuserRequiredMixin, CreateView):
    model = Categoria
    fields = ['nombre'] 
    template_name = 'libros/crear_autor.html' 
    success_url = reverse_lazy('lista_libros')

# 🚀 VISTA GENÉRICA (CreateView) - Crear Libro
class LibroCreateView(SuperuserRequiredMixin, CreateView):
    model = Libro
    fields = ['titulo', 'isbn', 'fecha_publicacion', 'autor', 'categoria']
    template_name = 'libros/libro_form.html'
    success_url = reverse_lazy('lista_libros') 

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
        return reverse_lazy('detalle_libro', kwargs={'slug': self.object.slug})

# 🚀 VISTA GENÉRICA (DeleteView) - Eliminar Libro
class LibroDeleteView(SuperuserRequiredMixin, DeleteView):
    model = Libro
    template_name = 'libros/libro_confirm_delete.html' 
    success_url = reverse_lazy('lista_libros')

# ----------------------------------------------------------------------
# --- VISTA DE AUTENTICACIÓN FIREBASE ---
# ----------------------------------------------------------------------

@require_POST
def firebase_login_view(request):
    """
    Recibe el token de ID de Firebase del cliente, lo verifica, sincroniza el usuario 
    con la base de datos de Django y autentica la sesión.
    """
    try:
        # Asegúrate de que el frontend envíe el token en el cuerpo JSON
        data = json.loads(request.body)
        id_token = data.get('id_token')
        
        if not id_token:
            return JsonResponse({'error': 'Token de ID no proporcionado.'}, status=400)

        # 1. Verificar y decodificar el token con el SDK Admin
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token.get('uid')
        email = decoded_token.get('email')
        
        # 2. Sincronizar usuario de Firebase con Usuario de Django
        try:
            # Busca al usuario existente por email
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Si no existe, crea un nuevo usuario de Django
            username = email.split('@')[0] if email else uid 
            user = User.objects.create_user(username=username, email=email)
            user.set_unusable_password() 
            user.save()

        # 3. Iniciar sesión en el contexto de Django
        login(request, user)
        
        return JsonResponse({
            'success': True, 
            'message': 'Autenticación exitosa.', 
            'redirect': reverse_lazy('lista_libros') 
        })

    except auth.InvalidIdTokenError:
        return JsonResponse({'error': 'Token de Firebase inválido o expirado.'}, status=401)
    except Exception as e:
        return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)