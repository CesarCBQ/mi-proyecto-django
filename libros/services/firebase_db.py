# libros/services/firebase_db.py

from firebase_admin import firestore

from libros.models import Libro


db = firestore.client()

def guardar_libro_en_firestore(libro_django: Libro):
    # Prepara los datos del modelo de Django
    data = {
        'titulo': libro_django.titulo,
        'autor_id': libro_django.autor.pk,
        # ... otros campos
    }
    
    # Guarda en Firestore usando el slug de Django como ID del documento
    db.collection('libros').document(libro_django.slug).set(data)
    print(f"Libro {libro_django.titulo} guardado en Firestore.")


def obtener_libro_de_firestore(slug):
    # Obtiene un documento
    doc = db.collection('libros').document(slug).get()
    if doc.exists:
        return doc.to_dict()
    return None