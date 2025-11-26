# usuarios/models.py

from django.db import models
from django.contrib.auth.models import User
from libros.models import Libro # Necesita el modelo Libro

# ... (Clase Perfil, si existe)

class Reseña(models.Model):
    # Relación One-to-Many: Un usuario hace muchas reseñas
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reseñas') 
    
    # Relación One-to-Many: Un libro tiene muchas reseñas
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='reseñas') 
    
    # Rating: Escala de 1 a 5
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    rating = models.IntegerField(choices=RATING_CHOICES) 
    
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 💥 ÉNFASIS: Solo una reseña por usuario por libro
        unique_together = ('usuario', 'libro') 
        verbose_name_plural = "Reseñas"

    def __str__(self):
        return f'Reseña de {self.usuario.username} para {self.libro.titulo}'