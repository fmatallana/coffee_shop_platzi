"""
============================================================================
DJANGO-ENVIRON PARA PROTEGER CREDENCIALES
============================================================================

CONCEPTOS FUNDAMENTALES
=======================

¿Qué es django-environ?
R: Librería que permite leer variables de entorno desde un archivo .env
   y usarlas dentro de settings.py para evitar exponer información sensible
   como contraseñas, tokens o URLs de bases de datos en el repositorio.

¿Qué es un archivo .env?
R: Archivo de texto plano que almacena variables de entorno del proyecto.
   Debe estar en la raíz del proyecto y nunca debe subirse al repositorio.
   Se debe agregar al .gitignore para proteger las credenciales.

¿Qué hace env.db()?
R: Método de django-environ que lee una variable de entorno con formato de URL
   de base de datos y la convierte automáticamente en el diccionario que
   Django necesita en DATABASES. Por ejemplo, esta URL:

   postgres://user:password@host:5432/dbname

   La convierte en este diccionario:

   {
       "ENGINE": "django.db.backends.postgresql",
       "NAME": "dbname",
       "HOST": "host",
       "PORT": "5432",
       "USER": "user",
       "PASSWORD": "password",
   }

¿Cuál es la estructura correcta de una URL de base de datos?
R: motor://usuario:contraseña@host:puerto/nombre_db

   Ejemplo:
   postgres://Db_username10:db_password@db-curso-django.crmwg00a8euf.us-east-2.rds.amazonaws.com:5432/postgres

¿Cuáles son las reglas para escribir valores en el archivo .env?
R: - No usar comillas alrededor del valor
   - No dejar espacios después del signo =
   - Correcto:   DJANGO_DB_URL=postgres://user:password@host:5432/db
   - Incorrecto: DJANGO_DB_URL= "postgres://user:password@host:5432/db"

¿Cuáles son las dos formas de cargar el archivo .env?
R: Desde código (recomendada): se define la ruta del archivo .env en settings.py
   y Django lo carga automáticamente al iniciar.
   Desde entorno: se exportan las variables manualmente en la terminal
   antes de correr el servidor. Es menos práctica para desarrollo local.


PASO A PASO - CONFIGURAR DJANGO-ENVIRON
=========================================

Paso 1: Instalar la librería

pip install django-environ


Paso 2: Importar y configurar en settings.py

import os
import environ

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

¿Qué hace environ.Env.read_env()?
R: Construye la ruta del archivo .env usando BASE_DIR como punto de partida
   y lo carga en memoria para que las variables estén disponibles en settings.py.


Paso 3: Crear el archivo .env en la raíz del proyecto

DJANGO_DB_URL=postgres://Db_username10:db_password@db-curso-django.crmwg00a8euf.us-east-2.rds.amazonaws.com:5432/postgres


Paso 4: Agregar .env al archivo .gitignore

.env


Paso 5: Actualizar DATABASES en settings.py

DATABASES = {"default": env.db("DJANGO_DB_URL")}


Paso 6: Verificar que la conexión funciona correctamente

./manage.py dbshell


CARGA DE VARIABLES DESDE ENTORNO (ALTERNATIVA)
================================================

En lugar de usar una URL completa, se pueden definir las credenciales
como variables separadas en el .env:

# .env
DJANGO_DB_PASSWORD=db_password
DJANGO_DB_USER=Db_username10

Y referenciarlas individualmente en settings.py:

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "HOST": "db-curso-django.crmwg00a8euf.us-east-2.rds.amazonaws.com",
        "PORT": "5432",
        "USER": env.str("DJANGO_DB_USER"),
        "PASSWORD": env.str("DJANGO_DB_PASSWORD"),
    }
}

O exportarlas manualmente desde la terminal antes de correr el servidor:

export DJANGO_DB_PASSWORD="db_password"
export DJANGO_DB_USER="Db_username10"

¿Cuándo usar esta alternativa?
R: Cuando se trabaja en un servidor o servicio en la nube que permite
   definir variables de entorno directamente en su configuración,
   sin necesidad de subir un archivo .env.
"""
