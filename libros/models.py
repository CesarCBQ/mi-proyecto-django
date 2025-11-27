from django.db import models
from django.urls import reverse 
from django.utils.text import slugify # 👈 IMPORTACIÓN AGREGADA AQUÍ

# --- 1. MODELO AUTOR (CORREGIDO) ---
class Autor(models.Model):
    # 🚨 CAMPOS AÑADIDOS
    nombre = models.CharField(max_length=100)
    biografia = models.TextField(blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Autores"

# --- 2. MODELO CATEGORIA (CORREGIDO) ---
class Categoria(models.Model):
    # 🚨 CAMPO AÑADIDO
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Categorías"

# --- 3. MODELO LIBRO (Ya estaba correcto, con get_absolute_url) ---
class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    fecha_publicacion = models.DateField()
    
    # Relaciones
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='libros') 
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='libros')
    
    # Campo slug
    slug = models.SlugField(max_length=200, unique=True, blank=True) 

    def __str__(self):
        return self.titulo
    
    # Para generar el slug automáticamente
    def save(self, *args, **kwargs):
        # La importación de slugify se movió al inicio del archivo para mayor limpieza
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    # MÉTODO DE REDIRECCIÓN
    def get_absolute_url(self):
        """Retorna la URL canónica del objeto Libro (su detalle)."""
        return reverse('detalle_libro', kwargs={'slug': self.slug})
    
    class Meta:
        verbose_name_plural = "Libros"