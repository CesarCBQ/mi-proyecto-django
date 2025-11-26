# libros/urls.py

from django.urls import path
from .views import LibroListView, detalle_libro, AutorCreateView
from .views_firebase import LibroListViewFirebase # <-- Nueva importación

urlpatterns = [
    # Versión Relacional (Postgres/SQLite)
    path('', LibroListView.as_view(), name='lista_libros'),
    path('<slug:slug>/', detalle_libro, name='detalle_libro'), 
    path('autor/nuevo/', AutorCreateView.as_view(), name='crear_autor'),
    
    # 🚀 VERSIÓN FIREBASE: Ruta alternativa
    path('firebase/', LibroListViewFirebase.as_view(), name='lista_libros_firebase'),
]