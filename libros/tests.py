from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify 
from .models import Autor, Categoria, Libro 
from django.db.utils import IntegrityError 


# ====================================================================
# I. CLASES DE PRUEBAS DE MODELOS (Modelos ya estaban correctos)
# ====================================================================

class CategoriaModelTest(TestCase):
    def setUp(self):
        Categoria.objects.create(nombre="Ficción Histórica")
        self.categoria = Categoria.objects.get(nombre="Ficción Histórica") 

    def test_categoria_creation(self):
        """1/3: Valida que la categoría se haya creado correctamente."""
        self.assertTrue(isinstance(self.categoria, Categoria))
        self.assertEqual(str(self.categoria), "Ficción Histórica")

    def test_categoria_slug(self):
        """2/3: Valida que el slug se genere correctamente."""
        self.assertEqual(self.categoria.slug, "ficcion-historica")
        
    def test_categoria_nombre_unique(self):
        """3/3: Valida que no se puedan crear dos categorías con el mismo nombre."""
        with self.assertRaises((IntegrityError, Exception)):
            Categoria.objects.create(nombre="Ficción Histórica")


class AutorModelTest(TestCase):
    def setUp(self):
        Autor.objects.create(nombre="Virginia Woolf")
        self.autor = Autor.objects.get(nombre="Virginia Woolf")

    def test_autor_creation(self):
        """1/3: Valida que el autor se haya creado correctamente."""
        self.assertTrue(isinstance(self.autor, Autor))
        self.assertEqual(str(self.autor), "Virginia Woolf")

    def test_autor_slug(self):
        """2/3: Valida que el slug se genere correctamente."""
        self.assertEqual(self.autor.slug, "virginia-woolf")

    def test_autor_related_name(self):
        """3/3: Valida que la relación inversa 'libros' del autor funcione."""
        self.assertEqual(self.autor.libros.count(), 0)


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
        self.libro.refresh_from_db() 

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
# II. CLASE DE PRUEBAS DE VISTAS (CORREGIDA: Uso de Namespaces y 'home')
# ====================================================================

class LibroViewTest(TestCase):
    def setUp(self):
        self.autor = Autor.objects.create(nombre="J.K. Rowling")
        self.categoria = Categoria.objects.create(nombre="Fantasía")
        
        # Creación masiva de libros con slugs y ISBN únicos
        for i in range(1, 16):
            titulo = f"Libro Test {i}"
            Libro.objects.create(
                titulo=titulo,
                slug=slugify(titulo), 
                isbn=f"978-0000000{i:05d}",
                fecha_publicacion="2020-01-01",
                autor=self.autor,
                categoria=self.categoria
            )
            
        self.libro_detalle = Libro.objects.get(titulo="Libro Test 1")
        self.libro_detalle.refresh_from_db()

        self.superuser = User.objects.create_superuser(username='admin', password='password123', email='admin@test.com')


    # --- Tests de LibroListView (3 tests) ---

    def test_lista_libros_status_code(self):
        """1/3: Valida que la página principal cargue correctamente (status 200)."""
        # 🚨 CORRECCIÓN: 'lista_libros' fue reemplazada por 'home' en el URLconf principal
        response = self.client.get(reverse('home')) 
        self.assertEqual(response.status_code, 200)

    def test_lista_libros_content(self):
        """2/3: Valida que la plantilla usada sea la correcta y contenga el título."""
        # 🚨 CORRECCIÓN: Usar 'home'
        response = self.client.get(reverse('home'))
        self.assertContains(response, self.libro_detalle.titulo)
        # La plantilla debe estar en libros/templates/libros/lista_libros.html
        self.assertTemplateUsed(response, 'libros/home.html')    
    def test_lista_libros_pagination(self):
        """3/3: Valida que la paginación funcione y muestre solo los primeros 10 libros."""
        # 🚨 CORRECCIÓN: Usar 'home'
        response = self.client.get(reverse('home'))
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(len(response.context['object_list']) == 10) # Usar object_list o el nombre de queryset
        self.assertNotContains(response, 'Libro Test 15')


    # --- Tests de detalle_libro (3 tests) ---

    def test_detalle_libro_success(self):
        """1/3: Valida que la página de detalle cargue con el slug correcto (status 200)."""
        # 🚨 CORRECCIÓN: Debe usar el namespace 'libros:detalle_libro'
        response = self.client.get(reverse('libros:detalle_libro', kwargs={'slug': self.libro_detalle.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'libros/detalle_libro.html')

    def test_detalle_libro_404(self):
        """2/3: Valida que se retorne 404 (No Encontrado) si el slug no existe."""
        # 🚨 CORRECCIÓN: Debe usar el namespace 'libros:detalle_libro'
        response = self.client.get(reverse('libros:detalle_libro', kwargs={'slug': 'libro-inexistente'}))
        self.assertEqual(response.status_code, 404)
        
    def test_detalle_libro_content_autor(self):
        """3/3: Valida que el autor relacionado se muestre correctamente en el contexto."""
        # 🚨 CORRECCIÓN: Debe usar el namespace 'libros:detalle_libro'
        response = self.client.get(reverse('libros:detalle_libro', kwargs={'slug': self.libro_detalle.slug}))
        self.assertContains(response, self.autor.nombre)
        self.assertEqual(response.context['libro'].autor.nombre, "J.K. Rowling")

    # --- Test de Seguridad (Extra) ---

    def test_crear_libro_redirect_anon(self):
        """Valida seguridad: Que un usuario anónimo sea redirigido al login."""
        # 🚨 CORRECCIÓN: Debe usar el namespace 'libros:crear_libro'
        response = self.client.get(reverse('libros:crear_libro'))
        self.assertEqual(response.status_code, 302)
        # La URL de login debe ser la definida en tu settings.py (LOGIN_URL) o la vista que redirige
        self.assertTrue(response.url.startswith('/accounts/login/') or response.url.startswith('/login/'))