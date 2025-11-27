from django.db import models
from django.urls import reverse 
from django.utils.text import slugify 
# 🟢 IMPORTACIÓN NECESARIA PARA FIREBASE/FIRESTORE 🟢
from firebase_admin import firestore 

# --- 1. MODELO AUTOR ---
class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    biografia = models.TextField(blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Autores"

# --- 2. MODELO CATEGORIA ---
class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Categorías"

# --- 3. MODELO LIBRO (Con integración de Firestore) ---
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
    
    # 🚀 MÉTODO SAVE: Sincroniza CREACIÓN y EDICIÓN con Firestore
    def save(self, *args, **kwargs):
        # 1. Aseguramos el slug
        if not self.slug:
            self.slug = slugify(self.titulo)

        # 2. 💾 Guardar primero en la base de datos de Django
        super().save(*args, **kwargs)

        # 3. 🚀 Sincronizar con Firestore
        try:
            db = firestore.client()
            # Usamos el PK de Django como ID del documento en la colección 'libros'
            doc_ref = db.collection('libros').document(str(self.pk))
            
            data = {
                'id_django': self.pk,
                'titulo': self.titulo,
                'slug': self.slug,
                'isbn': self.isbn,
                # Convertimos a formato ISO para compatibilidad JSON/Firestore
                'fecha_publicacion': self.fecha_publicacion.isoformat() if self.fecha_publicacion else None,
                # Incluimos nombres de las relaciones para facilitar consultas en Firestore
                'autor_nombre': self.autor.nombre if self.autor else 'Desconocido',
                'categoria_nombre': self.categoria.nombre if self.categoria else 'N/A'
            }
            
            # Guardar/Actualizar el documento
            doc_ref.set(data)
            
        except Exception as e:
            print(f"⚠️ ERROR de sincronización con Firestore para el libro {self.titulo}: {e}")

    # 🗑️ MÉTODO DELETE: Elimina el documento de Firestore
    def delete(self, *args, **kwargs):
        # 1. Intentamos eliminar de Firestore
        try:
            db = firestore.client()
            doc_ref = db.collection('libros').document(str(self.pk))
            doc_ref.delete()
        except Exception as e:
            print(f"⚠️ ERROR al eliminar de Firestore (ID: {self.pk}): {e}")
            
        # 2. Eliminar de la base de datos de Django
        super().delete(*args, **kwargs)

    # MÉTODO DE REDIRECCIÓN
    def get_absolute_url(self):
        """Retorna la URL canónica del objeto Libro (su detalle)."""
        return reverse('detalle_libro', kwargs={'slug': self.slug})
    
    class Meta:
        verbose_name_plural = "Libros"