"""
============================================================================
CREACIÓN DE LOGIN Y REGISTRO DE USUARIOS
============================================================================

CONCEPTOS FUNDAMENTALES
=======================

¿Qué es LoginView?
R: Vista genérica de Django que maneja todo el proceso de autenticación.
   Valida las credenciales del usuario y crea la sesión automáticamente.
   Solo requiere que se le indique el template a usar.

¿Qué es LOGIN_REDIRECT_URL?
R: Variable de settings.py que define a qué URL redirigir al usuario después de autenticarse.
   Se le pasa el nombre de la URL definido en urls.py.

LOGIN_REDIRECT_URL = "list_product"

¿Qué es {% csrf_token %}?
R: Tag de Django que genera un token de seguridad dentro de los formularios.
   Protege contra ataques Cross-Site Request Forgery (CSRF).
   Django rechaza cualquier formulario POST que no lo incluya.

¿Qué es crispy-forms?
R: Librería de terceros que mejora el renderizado visual de los formularios de Django.
   Permite aplicar estilos de frameworks CSS (como Tailwind) a los formularios
   sin necesidad de escribir HTML manualmente para cada campo.

¿Qué es UserCreationForm?
R: Formulario incluido en Django que maneja el registro de nuevos usuarios.
   Incluye validaciones de contraseña y unicidad de usuario de forma automática.

¿Cómo verificar que el login/logout funcionó correctamente?
R: Abrir las herramientas de desarrollo del navegador (F12),
   ir a la pestaña "Aplicación" y borrar las cookies.
   Al recargar la página el usuario quedará desautenticado.


PASO A PASO - CREAR LA APP DE USUARIOS
========================================

Paso 1: Crear la app

./manage.py startapp users


Paso 2: Registrar la app en settings.py

INSTALLED_APPS = [
    ...
    'users',
]


Paso 3: Crear urls.py en la app y registrarla en las urls globales

# users/urls.py
urlpatterns = [
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]

# urls globales
path("usuarios/", include("users.urls")),


Paso 4: Crear la carpeta de templates

users/
  templates/
    users/
      login.html
      register.html


Paso 5: Instalar y configurar crispy-forms con Tailwind

pip install crispy-tailwind
pip freeze > requirements.txt

# En settings.py agregar las apps (antes de las apps propias del proyecto)
INSTALLED_APPS = [
    ...
    "crispy_forms",
    "crispy_tailwind",
    "users",
]

# Al final de settings.py agregar
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

¿Por qué las apps de terceros van antes de las apps propias en INSTALLED_APPS?
R: Por convención y para evitar conflictos de carga.
   El orden recomendado es: apps de Django, apps de terceros, apps propias.


Paso 6: Crear login.html

{% extends "base.html" %}
{% load tailwind_filters %}

{% block content %}
<h1 class="text-3xl font-bold text-white">iniciar sesion</h1>

<form method="post">
    {% csrf_token %}
    {{ form|crispy }}
    <button type="submit" class="...">
        Login
    </button>
</form>
{% endblock content %}

¿Qué hace {% load tailwind_filters %}?
R: Carga las etiquetas y filtros de crispy-tailwind en el template.
   Es necesario para poder usar el filtro |crispy en el formulario.

¿Qué hace {{ form|crispy }}?
R: Renderiza todos los campos del formulario con los estilos de Tailwind aplicados automáticamente.


Paso 7: Agregar LOGIN_REDIRECT_URL en settings.py

LOGIN_REDIRECT_URL = "list_product"


Paso 8: Configurar la vista de registro en users/views.py

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("lazy")


Paso 9: Actualizar base.html para mostrar estado de autenticación

{% if user.is_authenticated %}
    <p>Hola, {{ user.username }}</p>
    <form method="post" action="{% url 'logout' %}">
        {% csrf_token %}
        <button type="submit">Log Out</button>
    </form>
{% else %}
    <p>Hola,</p>
    <a href="{% url 'login' %}">Iniciar Sesión</a>
{% endif %}

¿Qué es user.is_authenticated?
R: Propiedad que Django agrega automáticamente al objeto user en los templates.
   Retorna True si el usuario tiene una sesión activa, False si no está autenticado.
   Permite mostrar contenido diferente según el estado de autenticación.
"""
