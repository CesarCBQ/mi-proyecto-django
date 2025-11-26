# usuarios/views.py

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from libros.models import Libro
from .forms import ReseñaForm
# Importamos el modelo Reseña si lo necesitamos
# from .models import Reseña 

@login_required # Restringe el acceso: solo usuarios logueados
def crear_resena(request, libro_id):
    # 1. Obtener el libro al que se dirige la reseña (usa shortcut 404)
    libro = get_object_or_404(Libro, pk=libro_id) 

    if request.method == 'POST':
        form = ReseñaForm(request.POST)
        if form.is_valid():
            # 2. Asignar datos faltantes (usuario y libro)
            reseña = form.save(commit=False)
            reseña.usuario = request.user 
            reseña.libro = libro 
            
            # 3. Manejo de error de duplicado (si el usuario ya reseñó el libro)
            try:
                reseña.save()
            except Exception:
                # Opcional: agregar un mensaje flash
                pass 
                
            # 4. PRG Pattern: Redirige a la página del libro
            return redirect('detalle_libro', slug=libro.slug) 
    
    # Si no es POST o el formulario es inválido, redirige de vuelta al detalle
    return redirect('detalle_libro', slug=libro.slug)