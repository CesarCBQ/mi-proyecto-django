# libros/urls.py

from django.urls import path
from . import views 

# 🚨 CORRECCIÓN CRÍTICA: Definir app_name para usar namespaces.
app_name = 'libros' 

urlpatterns = [
    # -----------------------------------------------------------------
    # 🚀 1. RUTAS ESPECÍFICAS (CRUD, AUTH) - DEBEN IR PRIMERO
    # -----------------------------------------------------------------
    
    path('crear/', views.LibroCreateView.as_view(), name='crear_libro'),
    path('crear_autor/', views.AutorCreateView.as_view(), name='crear_autor'),
    path('crear_categoria/', views.CategoriaCreateView.as_view(), name='crear_categoria'),
    
    path('login/', views.login_page, name='login_page'), 
    
    path('editar/<slug:slug>/', views.LibroUpdateView.as_view(), name='editar_libro'),
    path('eliminar/<slug:slug>/', views.LibroDeleteView.as_view(), name='eliminar_libro'),

    # -----------------------------------------------------------------
    # 📝 2. RUTAS DINÁMICAS Y RAÍZ - DEBEN IR AL FINAL
    # -----------------------------------------------------------------
    
    # ¡IMPORTANTE! Mantener esta línea comentada o eliminada si 'home' la reemplazó:
    # path('', views.LibroListView.as_view(), name='lista_libros'),
    
    # Ruta Detalle de Libro 
    path('<slug:slug>/', views.detalle_libro, name='detalle_libro'), 
]