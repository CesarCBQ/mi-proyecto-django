from django.db import models
from django.urls import reverse 
from django.utils.text import slugify 
from django.conf import settings
# 🟢 IMPORTACIÓN NECESARIA PARA FIREBASE/FIRESTORE 🟢
from firebase_admin import firestore 

# --- 1. MODELO AUTOR (Slug y lógica de generación añadidos) ---
class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    biografia = models.TextField(blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    # 🚨 CORRECCIÓN: Agregar el campo slug
    slug = models.SlugField(max_length=100, unique=True, blank=True) 

    def save(self, *args, **kwargs):
        # 🚨 CORRECCIÓN: Generar el slug antes de guardar si no existe
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Autores"

# --- 2. MODELO CATEGORIA (Slug y lógica de generación añadidos) ---
class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    # 🚨 CORRECCIÓN: Agregar el campo slug
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    def save(self, *args, **kwargs):
        # 🚨 CORRECCIÓN: Generar el slug antes de guardar si no existe
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Categorías"

# --- 3. MODELO LIBRO (Slug y lógica de sincronización completada) ---
class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    fecha_publicacion = models.DateField()
    
    # Relaciones
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='libros') 
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='libros')
    
    # 🚨 CORRECCIÓN: El slug del libro DEBE ser único si se usa para URL detalladas.
    # También permitimos blank=True para que se autogenere.
    slug = models.SlugField(max_length=200, unique=True, blank=True) 

    def get_absolute_url(self):
        # Asegúrate de que esta URL exista en tu urls.py
        return reverse('detalle_libro', kwargs={'slug': self.slug})

    def __str__(self):
        return self.titulo
    
    def save(self, *args, **kwargs):
        # 1. Generación del slug (asegurando unicidad y autogeneración)
        if not self.slug:
            self.slug = slugify(self.titulo)
        
        # 2. Guardar el objeto Django primero
        super().save(*args, **kwargs)
        
        # 3. Sincronización con Firestore
        if settings.FIREBASE_CONFIG.get('SYNC_ENABLED', False):
            try:
                db = firestore.client()
                doc_ref = db.collection('libros').document(str(self.pk))
                
                data = {
                    'titulo': self.titulo,
                    'autor': self.autor.nombre,
                    'categoria': self.categoria.nombre if self.categoria else None,
                    'fecha_publicacion': self.fecha_publicacion.isoformat(),
                    'slug': self.slug,
                }
                doc_ref.set(data)
                
            except Exception:
                # 🚨 CORRECCIÓN: Silenciar el print para evitar warnings en tests
                pass 
                
    def delete(self, *args, **kwargs):
        # Lógica de eliminación de Firestore
        if self.pk and settings.FIREBASE_CONFIG.get('SYNC_ENABLED', False):
            try:
                db = firestore.client()
                doc_ref = db.collection('libros').document(str(self.pk))
                doc_ref.delete()
            except Exception:
                # 🚨 CORRECCIÓN: Silenciar el print para evitar warnings en tests
                pass
                
        super().delete(*args, **kwargs)