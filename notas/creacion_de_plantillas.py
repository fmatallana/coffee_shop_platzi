"""
============================================================================
CREACIÓN DE PLANTILLAS (TEMPLATES)
============================================================================

CONCEPTOS FUNDAMENTALES
=======================

¿Qué es base.html?
R: Template padre que contiene la estructura HTML común para todas las páginas.
   Las demás páginas extienden de él para reutilizar su estructura (head, nav, footer, estilos).
   Evita repetir código HTML en cada template del proyecto.

¿Qué es {% block content %}?
R: Etiqueta de Django que define una zona reemplazable en el template base.
   Los templates hijos sobreescriben este bloque con su propio contenido.
   Un template puede tener múltiples bloques con diferentes nombres.

¿Qué es {% extends %}?
R: Etiqueta que indica que un template hereda la estructura de otro.
   Debe ser la primera línea del template hijo.
   El template hijo solo define el contenido de los bloques que quiere sobreescribir.

¿Dónde busca Django los templates?
R: Por defecto, Django busca templates dentro de la carpeta templates/ de cada app.
   Para que Django también busque templates en una carpeta global fuera de las apps,
   se debe configurar la variable DIRS en settings.py.

¿Qué es DIRS en settings.py?
R: Lista de rutas absolutas donde Django buscará templates adicionales.
   Se usa para que el base.html creado fuera de las apps sea accesible desde todo el proyecto.


PASO A PASO - CONFIGURAR TEMPLATES
=====================================

Paso 1: Crear la carpeta de templates global

# Estructura recomendada
coffee_shop/        ← raíz del proyecto
  templates/
    base.html
  products/
  orders/
  users/


Paso 2: Configurar DIRS en settings.py para que Django encuentre el base.html global

import os

TEMPLATES = [
    {
        ...
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        ...
    }
]


Paso 3: Crear base.html con la estructura base

<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
</head>
<body>
    <div class="container mx-auto px-2">
        {% block content %}{% endblock content %}
    </div>
</body>
</html>


Paso 4: Extender desde base.html en los templates hijos

{% extends "base.html" %}
{% block content %}

    <!-- Contenido específico de esta página -->

{% endblock content %}


AGREGAR ESTILOS CON TAILWIND CSS
==================================

¿Cómo instalar Tailwind CSS en Django sin configuración adicional?
R: Usando el CDN de Tailwind. Solo se agrega una etiqueta script en el head de base.html.
   Es la opción más rápida para desarrollo. Para producción se recomienda la instalación completa.

<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>

¿Qué es Hyper UI?
R: Biblioteca de componentes HTML pre-diseñados y listos para usar con Tailwind CSS.
   Permite copiar bloques de código ya estilizados y adaptarlos reemplazando
   los datos de ejemplo por variables del template de Django.

Ejemplo de adaptación de un componente de Hyper UI:

# Código original de Hyper UI
<h3 class="mt-4 text-lg font-medium text-gray-900">robot</h3>

# Adaptado con variables de Django
<h3 class="mt-4 text-lg font-medium text-gray-900">{{ product.name }}</h3>


MOSTRAR IMÁGENES EN LOS TEMPLATES
====================================

¿Cómo mostrar una imagen solo si existe en el modelo?
R: Usando un condicional {% if %} para verificar que el campo de imagen no esté vacío.

{% if product.photo %}
    <img
        src="{{ product.photo.url }}"
        alt="{{ product.name }}"
        class="h-64 w-full object-cover"
    >
{% endif %}


OCULTAR CÓDIGO TEMPORALMENTE
================================

¿Cómo comentar bloques de código en los templates de Django?
R: Usando la etiqueta {% comment %} para ocultar secciones sin borrarlas.

{% comment %}
    <form class="mt-4">
        <button>Add to Cart</button>
    </form>
{% endcomment %}
"""
