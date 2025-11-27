# libros/urls.py

# 🟢 ¡CORRECCIÓN! Importamos 'path' para que el NameError no aparezca. 🟢
from django.urls import path
from . import views 

urlpatterns = [
    # -----------------------------------------------------------------
    # 🚀 1. RUTAS ESPECÍFICAS (CRUD, AUTH) - DEBEN IR PRIMERO
    # -----------------------------------------------------------------
    
    # --- URLs de Administración (CRUD) ---
    path('crear/', views.LibroCreateView.as_view(), name='crear_libro'),
    path('crear_autor/', views.AutorCreateView.as_view(), name='crear_autor'),
    path('crear_categoria/', views.CategoriaCreateView.as_view(), name='crear_categoria'),
    
    # --- URLs de Autenticación ---
    path('login/', views.login_page, name='login_page'), 
    path('auth/firebase/login/', views.firebase_login_view, name='firebase_login'),
    
    # --- URLs de Edición/Eliminación ---
    path('editar/<slug:slug>/', views.LibroUpdateView.as_view(), name='editar_libro'),
    path('eliminar/<slug:slug>/', views.LibroDeleteView.as_view(), name='eliminar_libro'),

    # -----------------------------------------------------------------
    # 📝 2. RUTAS DINÁMICAS Y RAÍZ - DEBEN IR AL FINAL
    # -----------------------------------------------------------------
    
    # Ruta Raíz (Lista de Libros)
    path('', views.LibroListView.as_view(), name='lista_libros'),
    
    # Ruta Detalle de Libro (La dinámica que debe ir al final)
    path('<slug:slug>/', views.detalle_libro, name='detalle_libro'), 
]