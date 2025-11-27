# libros/admin.py

from django.contrib import admin
from .models import Autor, Categoria, Libro 

# --- REGISTRO DE MODELOS ---

# 1. Registrar Categoria 
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    # Los campos de list_display son correctos según tu modelo
    list_display = ('nombre',)
    search_fields = ('nombre',)

# 2. Registrar Autor
@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    # Los campos de list_display son correctos según tu modelo
    list_display = ('nombre', 'fecha_nacimiento')
    search_fields = ('nombre',)

# 3. Registrar Libro
@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'categoria', 'isbn', 'fecha_publicacion') 
    list_filter = ('categoria', 'autor')
    search_fields = ('titulo', 'autor__nombre', 'isbn')
    
    # Genera automáticamente el slug basado en el título
    prepopulated_fields = {'slug': ('titulo',)} 
    
    # Lista de inlines vacía ya que ReseñaInline fue eliminado
    inlines = []