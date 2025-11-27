from unittest import TestCase
from django.urls import reverse
from django.contrib.auth.models import User # Necesario para test_crear_libro_redirect_anon

from libros.models import Autor, Categoria, Libro


class LibroViewTest(TestCase):
    def setUp(self):
        self.client = self.client
        self.autor = Autor.objects.create(nombre="J.K. Rowling")
        self.categoria = Categoria.objects.create(nombre="Fantasía")
        
        for i in range(1, 16):
            Libro.objects.create(
                titulo=f"Libro Test {i}",
                isbn=f"{i:013d}",
                fecha_publicacion="2020-01-01",
                autor=self.autor,
                categoria=self.categoria
            )
        self.libro_detalle = Libro.objects.get(titulo="Libro Test 1")
        self.superuser = User.objects.create_superuser(username='admin', password='password123', email='admin@test.com')


    def test_lista_libros_status_code(self):
        response = self.client.get(reverse('lista_libros'))
        self.assertEqual(response.status_code, 200)

    def test_lista_libros_content(self):
        response = self.client.get(reverse('lista_libros'))
        self.assertContains(response, self.libro_detalle.titulo)
        self.assertTemplateUsed(response, 'libros/lista_libros.html')
    
    def test_lista_libros_pagination(self):
        response = self.client.get(reverse('lista_libros'))
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(len(response.context['libros']) == 10)
        self.assertContains(response, 'Libro Test 1') 
        self.assertNotContains(response, 'Libro Test 15')

    def test_detalle_libro_success(self):
        response = self.client.get(reverse('detalle_libro', kwargs={'slug': self.libro_detalle.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Libro Test 1") 
        self.assertTemplateUsed(response, 'libros/detalle_libro.html')

    def test_detalle_libro_404(self):
        response = self.client.get(reverse('detalle_libro', kwargs={'slug': 'libro-inexistente'}))
        self.assertEqual(response.status_code, 404)
        
    def test_detalle_libro_content_autor(self):
        response = self.client.get(reverse('detalle_libro', kwargs={'slug': self.libro_detalle.slug}))
        self.assertContains(response, self.autor.nombre)
        self.assertEqual(response.context['libro'].autor.nombre, "J.K. Rowling")

    def test_crear_libro_redirect_anon(self):
        response = self.client.get(reverse('crear_libro'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))