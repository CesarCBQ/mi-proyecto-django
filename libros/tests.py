# libros/tests.py

from django.test import TestCase # ⬅️ CORRECCIÓN CRÍTICA: Usar TestCase de Django
from django.urls import reverse
from django.contrib.auth.models import User
# Asegúrate de que las importaciones de Modelos sean correctas:
from .models import Autor, Categoria, Libro 

# ====================================================================
# I. CLASES DE PRUEBAS DE MODELOS
# (Mínimo 3 tests por cada modelo: Categoria, Autor, Libro)
# ====================================================================

class CategoriaModelTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Ficción Histórica")

    def test_categoria_creation(self):
        """1/3: Valida que la categoría se haya creado correctamente."""
        self.assertTrue(isinstance(self.categoria, Categoria))
        self.assertEqual(str(self.categoria), "Ficción Histórica")

    def test_categoria_slug(self):
        """2/3: Valida que el slug se genere correctamente."""
        self.assertEqual(self.categoria.slug, "ficcion-historica")
        
    def test_categoria_nombre_unique(self):
        """3/3: Valida que no se puedan crear dos categorías con el mismo nombre."""
        # Se espera que falle al crear un duplicado (asumiendo unique=True en el modelo)
        with self.assertRaises(Exception):
             Categoria.objects.create(nombre="Ficción Histórica")


class AutorModelTest(TestCase):
    def setUp(self):
        self.autor = Autor.objects.create(nombre="Virginia Woolf")

    def test_autor_creation(self):
        """1/3: Valida que el autor se haya creado correctamente."""
        self.assertTrue(isinstance(self.autor, Autor))
        self.assertEqual(str(self.autor), "Virginia Woolf")

    def test_autor_slug(self):
        """2/3: Valida que el slug se genere correctamente."""
        self.assertEqual(self.autor.slug, "virginia-woolf")

    def test_autor_related_name(self):
        """3/3: Valida que la relación inversa 'libros' del autor funcione."""
        self.assertEqual(self.autor.libros.count(), 0) # Debe empezar en cero


class LibroModelTest(TestCase):
    def setUp(self):
        self.autor = Autor.objects.create(nombre="Gabriel García Márquez")
        self.categoria = Categoria.objects.create(nombre="Ficción")
        self.libro = Libro.objects.create(
            titulo="Cien años de soledad",
            isbn="9780307474728",
            fecha_publicacion="1967-05-30",
            autor=self.autor,
            categoria=self.categoria
        )

    def test_libro_creation(self):
        """1/3: El libro se crea correctamente y tiene un título."""
        self.assertTrue(isinstance(self.libro, Libro))
        self.assertEqual(str(self.libro), "Cien años de soledad")

    def test_libro_relation(self):
        """2/3: El libro está relacionado correctamente con el autor (ForeignKey)."""
        self.assertEqual(self.libro.autor.nombre, "Gabriel García Márquez")
        self.assertEqual(self.autor.libros.count(), 1)
    
    def test_slug_generation(self):
        """3/3: Verifica que el slug se genera correctamente."""
        expected_slug = "cien-anos-de-soledad"
        self.assertEqual(self.libro.slug, expected_slug)


# ====================================================================
# II. CLASE DE PRUEBAS DE VISTAS (VIEW TESTS)
# (Mínimo 3 tests para LibroListView y 3 para detalle_libro)
# ====================================================================

class LibroViewTest(TestCase):
    def setUp(self):
        # ❌ CORRECCIÓN: Se elimina la línea self.client = self.client
        # Django inicializa self.client automáticamente en TestCase.
        
        self.autor = Autor.objects.create(nombre="J.K. Rowling")
        self.categoria = Categoria.objects.create(nombre="Fantasía")
        
        # Crea 15 libros para probar la paginación 
        for i in range(1, 16):
            Libro.objects.create(
                titulo=f"Libro Test {i}",
                isbn=f"{i:013d}",
                fecha_publicacion="2020-01-01",
                autor=self.autor,
                categoria=self.categoria
            )
        self.libro_detalle = Libro.objects.get(titulo="Libro Test 1")
        
        # Necesario para el test de seguridad
        self.superuser = User.objects.create_superuser(username='admin', password='password123', email='admin@test.com')


    # --- Tests de LibroListView (3 tests) ---

    def test_lista_libros_status_code(self):
        """1/3: Valida que la página principal cargue correctamente (status 200)."""
        response = self.client.get(reverse('lista_libros'))
        self.assertEqual(response.status_code, 200)

    def test_lista_libros_content(self):
        """2/3: Valida que la plantilla usada sea la correcta y contenga el título."""
        response = self.client.get(reverse('lista_libros'))
        self.assertContains(response, self.libro_detalle.titulo)
        self.assertTemplateUsed(response, 'libros/lista_libros.html')
    
    def test_lista_libros_pagination(self):
        """3/3: Valida que la paginación funcione y muestre solo los primeros 10 libros."""
        response = self.client.get(reverse('lista_libros'))
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(len(response.context['libros']) == 10) # Asumiendo paginate_by = 10
        self.assertNotContains(response, 'Libro Test 15')


    # --- Tests de detalle_libro (3 tests) ---

    def test_detalle_libro_success(self):
        """1/3: Valida que la página de detalle cargue con el slug correcto (status 200)."""
        response = self.client.get(reverse('detalle_libro', kwargs={'slug': self.libro_detalle.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'libros/detalle_libro.html')

    def test_detalle_libro_404(self):
        """2/3: Valida que se retorne 404 (No Encontrado) si el slug no existe."""
        response = self.client.get(reverse('detalle_libro', kwargs={'slug': 'libro-inexistente'}))
        self.assertEqual(response.status_code, 404)
        
    def test_detalle_libro_content_autor(self):
        """3/3: Valida que el autor relacionado se muestre correctamente en el contexto."""
        response = self.client.get(reverse('detalle_libro', kwargs={'slug': self.libro_detalle.slug}))
        self.assertContains(response, self.autor.nombre)
        self.assertEqual(response.context['libro'].autor.nombre, "J.K. Rowling")

    # --- Test de Seguridad (Extra) ---

    def test_crear_libro_redirect_anon(self):
        """Valida seguridad: Que un usuario anónimo sea redirigido al login."""
        response = self.client.get(reverse('crear_libro'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))