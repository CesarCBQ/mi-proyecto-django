# core/views.py

from django.shortcuts import render

def home_view(request):
    # Vista para la página de inicio
    return render(request, 'base.html') 

def custom_404(request, exception):
    # Vista personalizada para el error 404
    return render(request, '404.html', {}, status=404)