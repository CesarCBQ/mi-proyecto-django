# libros/admin.py

from django.contrib import admin
from .models import Autor, Libro, Categoria
from usuarios.models import Reseña

# Inline para ver las reseñas directamente en el detalle del Libro
class ReseñaInline(admin.TabularInline):
    model = Reseña
    extra = 0 # No mostrar formularios vacíos por defecto

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    # Look 'n Feel en el listado
    list_display = ('titulo', 'autor', 'categoria', 'isbn', 'fecha_publicacion') 
    list_filter = ('categoria', 'autor', 'fecha_publicacion')
    search_fields = ('titulo', 'autor__nombre', 'isbn')
    prepopulated_fields = {'slug': ('titulo',)} # Ayuda a llenar el slug automáticamente
    
    # Tablas Relacionadas (Inlines)
    inlines = [ReseñaInline] 

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_nacimiento')
    search_fields = ('nombre',)
    
# Registrar los modelos restantes
admin.site.register(Categoria)
# admin.site.register(Reseña) # No lo registramos aquí porque usamos el inline