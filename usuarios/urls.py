# usuarios/urls.py (Crear este archivo)

from django.urls import path
from .views import crear_resena

app_name = 'usuarios' # Define un namespace para evitar colisiones

urlpatterns = [
    # Ruta para procesar el formulario de reseña
    path('resena/<int:libro_id>/crear/', crear_resena, name='crear_resena'),
]