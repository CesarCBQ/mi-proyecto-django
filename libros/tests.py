from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Autor, Categoria, Libro

# ====================================================================
# I. TESTS DE MODELOS (MODEL TESTS)
# ====================================================================

class CategoriaModelTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Ficción Histórica")

    def test_categoria_creation(self):
        """Valida que la categoría se haya creado correctamente."""
        self.assertTrue(isinstance(self.categoria, Categoria))
        self.assertEqual(str(self.categoria), "Ficción Histórica")

    def test_categoria_slug(self):
        """Valida que el slug se genere correctamente a partir del nombre."""
        self.assertEqual(self.categoria.slug, "ficcion-historica")
        
    def test_categoria_nombre_unique(self):
        """Valida que no se puedan crear dos categorías con el mismo nombre."""
        # Intentamos crear una segunda categoría con el mismo nombre
        with self.assertRaises(Exception):
             Categoria.objects.create(nombre="Ficción Histórica")


class AutorModelTest(TestCase):
    def setUp(self):
        self.autor = Autor.objects.create(nombre="Virginia Woolf")

    def test_autor_creation(self):
        """Valida que el autor se haya creado correctamente."""
        self.assertTrue(isinstance(self.autor, Autor))
        self.assertEqual(str(self.autor), "Virginia Woolf")

    def test_autor_slug(self):
        """Valida que el slug se genere correctamente a partir del nombre."""
        self.assertEqual(self.autor.slug, "virginia-woolf")

    def test_autor_related_name(self):
        """Valida que el related_name 'libros' del autor funcione."""
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
        """El libro se crea correctamente y tiene un título."""
        self.assertTrue(isinstance(self.libro, Libro))
        self.assertEqual(str(self.libro), "Cien años de soledad")

    def test_libro_relation(self):
        """El libro está relacionado correctamente con el autor."""
        self.assertEqual(self.libro.autor.nombre, "Gabriel García Márquez")
        self.assertEqual(self.autor.libros.count(), 1) # Prueba la related_name
    
    def test_slug_generation(self):
        """Verifica que el slug se genera correctamente."""
        expected_slug = "cien-anos-de-soledad"
        self.assertEqual(self.libro.slug, expected_slug)


# ====================================================================
# II. TESTS DE VISTAS (VIEW TESTS)
# ====================================================================

class LibroViewTest(TestCase):
    def setUp(self):
        self.client = self.client # Cliente de pruebas de Django
        self.autor = Autor.objects.create(nombre="J.K. Rowling")
        self.categoria = Categoria.objects.create(nombre="Fantasía")
        self.libro = Libro.objects.create(
            titulo="Harry Potter y la Piedra Filosofal",
            isbn="1234567890123",
            fecha_publicacion="1997-06-26",
            autor=self.autor,
            categoria=self.categoria
        )
        self.superuser = User.objects.create_superuser(username='admin', password='password123', email='admin@test.com')

    # --- Tests de LibroListView ---

    def test_lista_libros_status_code(self):
        """Valida que la página principal (lista de libros) cargue correctamente (status 200)."""
        response = self.client.get(reverse('lista_libros')) # Usamos reverse() para obtener la URL
        self.assertEqual(response.status_code, 200)

    def test_lista_libros_content(self):
        """Valida que el libro creado esté presente en el contexto de la plantilla."""
        response = self.client.get(reverse('lista_libros'))
        self.assertContains(response, self.libro.titulo)
        self.assertTemplateUsed(response, 'libros/lista_libros.html')

    # --- Tests de detalle_libro ---

    def test_detalle_libro_success(self):
        """Valida que la página de detalle cargue con el slug correcto."""
        response = self.client.get(reverse('detalle_libro', kwargs={'slug': self.libro.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Harry Potter y la Piedra Filosofal")

    def test_detalle_libro_404(self):
        """Valida que se retorne 404 (No Encontrado) si el slug no existe."""
        response = self.client.get(reverse('detalle_libro', kwargs={'slug': 'libro-inexistente'}))
        self.assertEqual(response.status_code, 404)

    # --- Tests de Seguridad (requiere SuperuserRequiredMixin en las vistas) ---

    def test_crear_libro_redirect_anon(self):
        """Valida que un usuario anónimo sea redirigido al login al intentar acceder a la vista de creación."""
        response = self.client.get(reverse('crear_libro'))
        # 302 es el código de redirección. La URL final es la de login.
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))