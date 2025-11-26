from django.db import models

class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    biografia = models.TextField(blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Autores"

class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Categorías"

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    fecha_publicacion = models.DateField()
    
    # Relación One-to-Many con Autor
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='libros') 
    
    # Relación Many-to-One con Categoría
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='libros')
    
    # Para la URL dinámica con slug
    slug = models.SlugField(max_length=200, unique=True, blank=True) 

    def __str__(self):
        return self.titulo
    
    # Opcional: Para generar el slug automáticamente
    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)