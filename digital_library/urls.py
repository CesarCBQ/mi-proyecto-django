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
# Importamos la vista del core para la página de inicio (la crearemos más adelante)
from core.views import home_view 
from django.conf.urls import handler404 # Importamos handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('libros/', include('libros.urls')), # Incluimos las URLs de la app 'libros'
    path('usuarios/', include('usuarios.urls')), # Incluimos las URLs de la app 'usuarios'
]

# Manejo de Error 404
# Apuntamos a una vista personalizada (la crearemos en core/views.py)
handler404 = 'core.views.custom_404'