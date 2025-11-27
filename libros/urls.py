# libros/urls.py

from django.urls import path
from . import views # Asegúrate de importar tu archivo views.py

urlpatterns = [
    # --- URLs de Lectura ---
    path('', views.LibroListView.as_view(), name='lista_libros'),
    path('<slug:slug>/', views.detalle_libro, name='detalle_libro'),
    
    # --- URLs de Administración (CRUD) ---
    path('crear/', views.LibroCreateView.as_view(), name='crear_libro'),
    path('editar/<slug:slug>/', views.LibroUpdateView.as_view(), name='editar_libro'),
    path('eliminar/<slug:slug>/', views.LibroDeleteView.as_view(), name='eliminar_libro'),

    # Estas rutas son solo ejemplos, asume que existen
    path('crear_autor/', views.AutorCreateView.as_view(), name='crear_autor'),
    path('crear_categoria/', views.CategoriaCreateView.as_view(), name='crear_categoria'),
    
    # 🔑 URL DE INTEGRACIÓN FIREBASE AUTH 🔑
    # Esta ruta recibirá el token de ID del frontend
    path('auth/firebase/login/', views.firebase_login_view, name='firebase_login'),
]