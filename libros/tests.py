# libros/tests.py

from django.test import TestCase
from .models import Autor, Categoria, Libro

class LibroModelTest(TestCase):
    def setUp(self):
        # Configuración inicial para los tests
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

# Ejecutar tests: python manage.py test