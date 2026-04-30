"""
============================================================================
CONFIGURAR BASES DE DATOS CON DJANGO Y AWS RDS
============================================================================

CONCEPTOS FUNDAMENTALES
=======================

¿Por qué no usar SQLite en producción?
R: SQLite no está diseñada para manejar muchas conexiones simultáneas.
   Es adecuada solo para desarrollo local o proyectos pequeños.
   Para producción se necesita una base de datos como PostgreSQL, que es
   más rápida, estable y soporta múltiples conexiones concurrentes.

¿Qué es psycopg2?
R: Librería que actúa como puente entre Django y PostgreSQL.
   Django genera las queries internamente pero las envía a la base de datos
   a través de psycopg2, que las formatea correctamente y devuelve
   la respuesta como un diccionario o estructura usable por Python.

¿Por qué se instala psycopg2-binary y no psycopg2?
R: psycopg2 es una librería compilada, lo que significa que necesita
   herramientas del sistema (como gcc) para instalarse desde el código fuente.
   La versión -binary viene precompilada y no requiere esas dependencias.
   Para desarrollo se recomienda -binary. Para producción se recomienda
   compilar desde el código fuente porque es más estable.

¿Cómo saber si una librería necesita la versión -binary?
R: Si al hacer pip install nombre_libreria aparece un error como:
   "pg_config executable not found" o "error: command 'gcc' failed",
   es señal de que la librería necesita compilarse.
   En ese caso buscar si existe una versión nombre_libreria-binary.

¿Por qué usar el mismo motor de base de datos en local y en producción?
R: Para evitar problemas de compatibilidad entre entornos.
   Si se usa SQLite en local y PostgreSQL en producción, pueden aparecer
   errores que no se detectan durante el desarrollo.

¿Por qué usar AWS RDS?
R: Es un servicio administrado de bases de datos en la nube.
   AWS se encarga del mantenimiento, backups y disponibilidad del servidor,
   lo que lo hace más estable y confiable que administrar una BD propia.


PASO A PASO - INSTALAR Y CONFIGURAR POSTGRESQL EN LOCAL
=========================================================

Paso 1: Instalar PostgreSQL

sudo apt install postgresql


Paso 2: Instalar el adaptador de Python para PostgreSQL

pip install psycopg2-binary


Paso 3: Acceder al usuario administrador del sistema

sudo -i -u postgres

¿Por qué este paso?
R: PostgreSQL crea automáticamente un usuario del sistema llamado postgres
   con acceso total. Se accede a él para poder administrar la BD
   sin necesitar contraseña todavía.


Paso 4: Entrar a la consola de PostgreSQL

psql


Paso 5: Asignarle una contraseña al superusuario postgres

ALTER USER postgres PASSWORD 'nueva_contraseña';


Paso 6: Crear la base de datos del proyecto

CREATE DATABASE postgres_local;


Paso 7: Crear el usuario con el que Django se conectará

CREATE USER matallana WITH PASSWORD 'tu_contraseña';


Paso 8: Darle permisos completos al usuario sobre la base de datos

GRANT ALL PRIVILEGES ON DATABASE postgres_local TO matallana;


Paso 9: Verificar que la base de datos fue creada correctamente

\l


Paso 10: Salir de la consola de PostgreSQL y del usuario postgres

exit


Paso 11: Verificar la conexión desde fuera como superusuario

psql -h localhost -U postgres -d postgres_local


Paso 12: Verificar que Django puede conectarse correctamente

./manage.py dbshell


CONFIGURACIÓN EN SETTINGS.PY
==============================

Configuración para base de datos local:

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres_local",
    }
}

Configuración para base de datos en producción (AWS RDS):

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "HOST": "db-curso-django.crmwg00a8euf.us-east-2.rds.amazonaws.com",
        "PORT": "5432",
        "USER": "Db_username10",
        "PASSWORD": "db_password",
    }
}

¿De dónde se sacan los datos de la configuración de producción?
R: Del panel de AWS RDS, en la página de detalles de la instancia creada.
   El HOST es el endpoint que AWS asigna automáticamente a la instancia.

⚠️ IMPORTANTE: Las credenciales nunca deben estar directamente en settings.py
   en un proyecto real. Se deben usar variables de entorno para protegerlas (LEER COMO SE HACE EN django_environ_para_credenciales.py).


PASO A PASO - CREAR BASE DE DATOS EN AWS RDS
=============================================

Paso 1: Buscar RDS en la consola de AWS y hacer click en "Bases de datos"

Paso 2: Click en "Crear base de datos" y seleccionar "Configuración completa"
        No usar "Creación sencilla" ya que limita las opciones de configuración.

Paso 3: Seleccionar PostgreSQL como motor de base de datos
        Debe coincidir con el motor usado en local para evitar incompatibilidades.

Paso 4: Seleccionar "Free tier" en las plantillas

Paso 5: Configurar los datos de la instancia:
        - Identificador de instancia: db-curso-django
        - Nombre de usuario maestro: Db_username10
        - Contraseña: db_password

Paso 6: Seleccionar db.t3.micro como tipo de instancia
        Es la única clase incluida en el free tier. Otras clases como
        db.t4g.micro pueden generar costos inesperados.

Paso 7: En la sección Conectividad:
        - Seleccionar "No conectarse a un recurso EC2"
        - Cambiar "Acceso público" a Sí para poder conectarse desde local

Paso 8: Click en "Crear base de datos" y esperar a que el estado sea "Available"


CONFIGURACIÓN DE REGLAS DE SEGURIDAD EN AWS
============================================

Paso 1: Click en el nombre de la instancia RDS creada

Paso 2: En la sección Seguridad, click en el Security Group (default sg)

Paso 3: Click en "Reglas de entrada" → "Editar reglas de entrada"

Paso 4: Agregar una nueva regla con estos ajustes:
        - Tipo: Todo el tráfico
        - Origen: My IP (solo permite conexiones desde tu IP actual)

Paso 5: Guardar las reglas

¿Por qué configurar las reglas de entrada?
R: Por defecto AWS bloquea todo el tráfico externo hacia la base de datos.
   Sin esta regla no es posible conectarse desde la máquina local aunque
   la base de datos esté configurada como pública.
"""
