"""
URL configuration for digital_library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# digital_library/urls.py

from django.contrib import admin
from django.urls import path, include

# Importamos la vista específica de la lista de libros 
# para poder nombrar la ruta raíz como 'home' directamente.
# Suponiendo que LibroListView está en libros.views
from libros.views import LibroListView 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 🚨 CORRECCIÓN 1: Definir explícitamente la raíz como 'home'.
    # Apuntamos la ruta base ('') directamente a la vista, dándole el nombre 'home'.
    path('', LibroListView.as_view(), name='home'),
    
    # 🚨 CORRECCIÓN 2: Incluir las URLs de 'libros/' bajo un prefijo,
    # para que las rutas CRUD/Detalle no colisionen con 'home'.
    # Si la ruta raíz (home) ya maneja la lista de libros, 
    # movemos las demás URLs de libros a un prefijo.
    path('libros/', include('libros.urls', namespace='libros')), 
]