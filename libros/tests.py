# libros/tests.py - SOLO LA CLASE DE VISTAS AMPLIADA

from unittest import TestCase
from django.urls import reverse

from libros.models import Autor, Categoria, Libro


class LibroViewTest(TestCase):
    def setUp(self):
        self.client = self.client
        self.autor = Autor.objects.create(nombre="J.K. Rowling")
        self.categoria = Categoria.objects.create(nombre="Fantasía")
        
        # Crea 15 libros para probar la paginación (si paginate_by = 10)
        for i in range(1, 16):
            Libro.objects.create(
                titulo=f"Libro Test {i}",
                isbn=f"{i:013d}",
                fecha_publicacion="2020-01-01",
                autor=self.autor,
                categoria=self.categoria
            )
        # El libro clave para el detalle:
        self.libro_detalle = Libro.objects.get(titulo="Libro Test 1")


    # --- Tests de LibroListView (Ahora son 3) ---

    def test_lista_libros_status_code(self):
        """Valida 1/3: Que la página principal cargue correctamente (status 200)."""
        response = self.client.get(reverse('lista_libros'))
        self.assertEqual(response.status_code, 200)

    def test_lista_libros_content(self):
        """Valida 2/3: Que la plantilla usada sea la correcta y contenga el título."""
        response = self.client.get(reverse('lista_libros'))
        self.assertContains(response, self.libro_detalle.titulo)
        self.assertTemplateUsed(response, 'libros/lista_libros.html')
    
    def test_lista_libros_pagination(self):
        """Valida 3/3: Que la paginación funcione y muestre solo los primeros 10 libros."""
        response = self.client.get(reverse('lista_libros'))
        # Asumiendo paginate_by = 10, la primera página debe tener 10 objetos
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(len(response.context['libros']) == 10) # Comprueba la paginación
        self.assertContains(response, 'Libro Test 1') 
        self.assertNotContains(response, 'Libro Test 15') # El último no debe estar en la pág 1

    # --- Tests de detalle_libro (Ahora son 3) ---

    def test_detalle_libro_success(self):
        """Valida 1/3: Que la página de detalle cargue con el slug correcto (status 200)."""
        response = self.client.get(reverse('detalle_libro', kwargs={'slug': self.libro_detalle.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Libro Test 1") # Título del libro
        self.assertTemplateUsed(response, 'libros/detalle_libro.html')

    def test_detalle_libro_404(self):
        """Valida 2/3: Que se retorne 404 (No Encontrado) si el slug no existe."""
        response = self.client.get(reverse('detalle_libro', kwargs={'slug': 'libro-inexistente'}))
        self.assertEqual(response.status_code, 404)
        
    def test_detalle_libro_content_autor(self):
        """Valida 3/3: Que el autor relacionado se muestre correctamente en el contexto."""
        response = self.client.get(reverse('detalle_libro', kwargs={'slug': self.libro_detalle.slug}))
        self.assertContains(response, self.autor.nombre)
        self.assertEqual(response.context['libro'].autor.nombre, "J.K. Rowling")

    # --- Tests de Seguridad (Dejarlo ya que valida una vista de la aplicación) ---

    def test_crear_libro_redirect_anon(self):
        """Valida que un usuario anónimo sea redirigido al login al intentar acceder a la vista de creación."""
        response = self.client.get(reverse('crear_libro'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))