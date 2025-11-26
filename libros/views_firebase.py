# libros/views_firebase.py

from django.shortcuts import render
from django.views.generic import View # Usamos View simple en lugar de ListView
from digital_library.firebase_config import get_firebase_db 
# from .forms import ReseñaForm # Necesitarías adaptarlo para Firebase

class LibroListViewFirebase(View):
    template_name = 'libros/templates/libros/lista_libros_firebase.html'

    def get(self, request, *args, **kwargs):
        db = get_firebase_db()
        
        # 1. Obtener datos de la colección 'libros'
        libros_ref = db.collection('libros')
        
        # 2. Convertir los documentos de Firebase a una lista de diccionarios Python
        libros_list = []
        for doc in libros_ref.stream():
            libro_data = doc.to_dict()
            libro_data['id'] = doc.id # Usar el ID del documento como clave
            libros_list.append(libro_data)

        context = {
            'libros': libros_list,
            'is_firebase': True # Para diferenciar la versión en el template
        }
        return render(request, self.template_name, context)