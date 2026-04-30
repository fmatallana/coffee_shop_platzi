"""
============================================================================
CONFIGURACIÓN INICIAL DE UN PROYECTO DJANGO
============================================================================

CONCEPTOS FUNDAMENTALES
=======================

¿Qué es un entorno virtual?
R: Un aislamiento de Python donde instalas dependencias específicas para tu proyecto.
   Cada proyecto tiene sus propias librerías independientes, sin afectar el sistema.

¿Por qué necesito un entorno virtual?
R: Evita conflictos entre versiones de librerías.
   Proyecto A puede usar Django 3.0, Proyecto B puede usar Django 4.0 sin problemas.

¿Qué es un requisito (requirements)?
R: Un archivo que lista todas las dependencias (librerías) que tu proyecto necesita.
   requirements.txt = dependencias para producción
   requirements-dev.txt = dependencias solo para desarrollo (testing, debugging)


PASO A PASO - CREAR Y CONFIGURAR UN PROYECTO DJANGO
====================================================

Paso 1: Crear y activar entorno virtual

# Crear el entorno (se llama venv por convención)
python -m venv venv

# Activar el entorno (en Linux/Mac)
source venv/bin/activate

# Activar el entorno (en Windows)
venv\Scripts\activate


¿Cómo sé si el entorno está activado?
R: Verás (venv) antes del comando en la terminal: (venv) user@computer:~$


Paso 2: Instalar Django

pip install django

¿Qué es pip?
R: Package Installer for Python. Descarga e instala librerías de Python desde internet.


Paso 3: Crear la estructura del proyecto

django-admin startproject coffee_shop .

¿Qué hace django-admin startproject?
R: Crea la carpeta base del proyecto con archivos de configuración necesarios.
   El punto (.) significa "crear aquí", no crea una carpeta extra.

Crea:
  - manage.py: archivo para ejecutar comandos Django
  - coffee_shop/: carpeta de configuración
    - settings.py: configuración del proyecto
    - urls.py: rutas principales
    - wsgi.py: para desplegar en servidores


Paso 4: Iniciar repositorio Git

git init

¿Por qué?
R: Controlar versiones del código. Guardar historial de cambios.

git add .
git commit -m "Inicial commit - Django structure"


Paso 5: Crear .gitignore

# Descargar desde https://www.gitignore.io
# Buscar "django" y copiar el contenido

¿Qué es .gitignore?
R: Archivo que le dice a Git qué archivos NO subir al repositorio.
   Típicamente: db.sqlite3, venv/, __pycache__/, .env

Ejemplo de contenido:
venv/
*.pyc
__pycache__/
db.sqlite3
.env
*.log


Paso 6: Crear requirements.txt

# Guarda las dependencias actuales
pip freeze > requirements.txt

¿Qué hace pip freeze?
R: Lista todas las librerías instaladas con sus versiones exactas.

Contenido típico:
Django==4.2.0
Pillow==10.0.0
sqlparse==0.4.4


¿Por qué no debo agregar todas las dependencias de las dependencias?
R: pip freeze lista TODO, incluyendo las dependencias de Django (asgiref, sqlparse, etc).
   Cuando alguien instale tu proyecto con pip install -r requirements.txt, pip descarga automáticamente las dependencias de las dependencias.
   Mantener solo las librerías que usas directamente hace el archivo más limpio.


Paso 7: Crear requirements-dev.txt

# Este archivo enlaza requirements.txt y agrega lo de desarrollo
-r requirements.txt
ipython==9.0.0
django-extensions==3.2.0

¿Cuál es la diferencia entre requirements.txt y requirements-dev.txt?
R:
  - requirements.txt: lo que necesitas en producción (servidor real)
  - requirements-dev.txt: lo que necesitas en desarrollo (tu computadora)

  Desarrollo incluye herramientas como IPython (consola mejorada) que no necesitas en el servidor.

¿Cómo instalo las dependencias?
R:
  # En desarrollo (instala todo)
  pip install -r requirements-dev.txt

  # En producción (solo lo necesario)
  pip install -r requirements.txt


Paso 8: Crear una app dentro del proyecto

python manage.py startapp products

¿Qué es una app en Django?
R: Un módulo funcional dentro del proyecto. Un proyecto puede tener varias apps.
   Ejemplo: proyecto = "tienda", apps = "productos", "usuarios", "pagos"

Crea:
  - products/models.py: define la estructura de datos
  - products/views.py: lógica de qué mostrar
  - products/urls.py: rutas específicas de la app
  - products/admin.py: configuración del panel admin


Paso 9: Registrar la app en settings.py

# En coffee_shop/settings.py, en INSTALLED_APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    # ... otras apps de Django
    'products',  # Agregar aquí
]


¿Por qué debo registrar la app?
R: Django necesita saber qué apps hacen parte del proyecto.
   Sin esto, Django no carga modelos, migraciones, ni configuración de la app.


FLUJO COMPLETO DE INSTALACIÓN
==============================

1. Crear entorno: python -m venv venv
2. Activar entorno: source venv/bin/activate
3. Instalar Django: pip install django
4. Crear proyecto: django-admin startproject coffee_shop .
5. Iniciar Git: git init
6. Crear .gitignore
7. Generar requirements: pip freeze > requirements.txt
8. Crear requirements-dev: agregar -r requirements.txt e ipython
9. Crear app: python manage.py startapp products
10. Registrar app: agregar 'products' en INSTALLED_APPS
11. Hacer migraciones iniciales: python manage.py migrate
12. Probar servidor: python manage.py runserver


¿Qué es una migración?
R: Un archivo que registra cambios en la estructura de la BD.
   Las migraciones permiten versionar la BD como si fuera código.

python manage.py migrate: ejecuta todas las migraciones pendientes
python manage.py makemigrations: crea nuevas migraciones basadas en cambios en models.py
"""
