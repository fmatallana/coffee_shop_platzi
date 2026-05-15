"""
============================================================================
DESPLIEGUE DE PROYECTO (AWS ELASTIC BEANSTALK)
============================================================================

CONCEPTOS FUNDAMENTALES
=======================

¿Qué es AWS Elastic Beanstalk (EB)?
R: Es un servicio de AWS al que se le envía el código y él se encarga de crear,
   gestionar y provisionar toda la infraestructura necesaria (servidores, redes, etc.)
   por nosotros. Se puede usar mediante la consola web o consola de comandos (CLI).

¿Qué es el archivo requirements.txt?
R: Es un archivo que contiene la lista exacta de todas las librerías y dependencias
   (con sus versiones) que necesita el proyecto para funcionar. Al hacer el despliegue,
   AWS lee este archivo para instalar todo correctamente en el servidor.

¿Por qué las credenciales (como DJANGO_DB_URL) van en un archivo .env?
R: Por seguridad estricta. El archivo .env contiene información sensible (contraseñas,
   claves secretas, URLs de bases de datos reales). NUNCA debe subirse a un repositorio
   (debe estar en el .gitignore) porque si el repositorio es público o sufre una
   vulnerabilidad, se expondrían directamente las bases de datos o cuentas de AWS.

¿Qué es Black?
R: Es una librería de Python que funciona como un formateador de código estricto.
   Permite mantener exactamente el mismo estilo y formato en todos los archivos del proyecto.

¿Qué es WSGI?
R: Web Server Gateway Interface. En Django, es el archivo (wsgi.py) que sirve como
   puente de comunicación entre tu aplicación en Python y el servidor web de producción
   que utiliza AWS.


============================================================================
PASO A PASO: PREPARACIÓN DEL PROYECTO LOCAL
============================================================================

Paso 1: Ajustar las URLs globales
En lugar de tener una ruta específica, se configura para que al abrir la URL base,
cargue directamente la lista de productos (así el usuario ve contenido de inmediato).

Antes: path("/products", include("products.urls"))
Ahora: path("", include("products.urls"))

*Nota: Es importante poner esta ruta en la parte superior del archivo urls.py, ya que
Django evalúa las URLs en orden.*

Paso 2: Formatear el código
pip install black
black .

Paso 3: Generar el archivo de requerimientos
Para guardar las versiones exactas que tienes instaladas en tu entorno local:
pip freeze > requirements.txt

Paso 4: Recolectar archivos estáticos
Para que los estilos (CSS), imágenes y JavaScript se empaqueten listos para producción:
python manage.py collectstatic

Paso 5: Crear archivo README.md
Es una buena práctica crear un archivo README en la raíz para documentar el proyecto.


============================================================================
PASO A PASO: CONFIGURACIÓN DE AWS (CREDENCIALES)
============================================================================

Paso 1: Crear Usuario IAM
1. Entrar a la consola de AWS -> IAM -> Users -> Create user.
2. Seleccionar "Anexar políticas directamente" (Attach policies directly).
3. Seleccionar "AdministratorAccess".
   *Nota: Esto se hace como método rápido por facilidad para el despliegue, pero es
   muy aconsejable revisar y limitar los permisos en entornos empresariales reales.*
4. Clic en Next y Create User.

Paso 2: Generar Credenciales
1. Clic en el nombre del usuario recién creado.
2. Ir a la pestaña "Security credentials" -> "Create access key".
3. Elegir la opción de consola: "Command Line Interface (CLI)".
4. Confirmar el check abajo, dar Next y crear. (Guardar estas llaves).


============================================================================
PASO A PASO: DESPLIEGUE CON EB CLI
============================================================================

Paso 1: Instalar la herramienta de consola de Elastic Beanstalk
pip install awsebcli

Paso 2: Inicializar el entorno
eb init
(Sigue las instrucciones en consola para enlazar el proyecto a tu cuenta de AWS)

Paso 3: Configurar Variables de Entorno en AWS (IMPORTANTE)
Como el archivo .env no se sube a GitHub ni a AWS por seguridad, debes inyectar
la URL de tu base de datos manualmente en el entorno de Elastic Beanstalk usando
la siguiente estructura genérica:

eb setenv DJANGO_DB_URL="postgres://USUARIO:PASSWORD@HOST:PUERTO/DB"

Paso 4: Hacer el Deploy
eb deploy <nombre-de-tu-entorno-production>

Paso 5: Ejecutar migraciones en el servidor
Para entrar al servidor, activar el entorno y correr las tablas de la base de datos:
eb ssh
(Luego ejecutas las migraciones tradicionales de Django dentro de la terminal de AWS)


============================================================================
RESOLUCIÓN DE ERRORES (TROUBLESHOOTING)
============================================================================

Error 1: AWS no encuentra la aplicación (El despliegue falla)
Causa: AWS busca por defecto un archivo llamado "application", pero en Django la
aplicación se encuentra encapsulada dentro del archivo "wsgi.py".
Solución:
1. Ejecutar en consola: eb config
2. Buscar la línea que dice "WSGIPath" (por defecto dirá application).
3. Cambiarlo a: nombre_de_tu_proyecto.wsgi:application (ej. coffee_shop.wsgi:application).
4. Guardar (Ctrl+O, Enter, Ctrl+X).
5. Verificar con "eb status" si se arregló, o ejecutar "eb logs" para más detalles.

Error 2: Falla la base de datos por credenciales (DJANGO_DB_URL)
Causa 1: Olvidaste ejecutar el comando "eb setenv" para inyectar la URL.
Causa 2: Usaste caracteres especiales en la contraseña de la DB (como el "#").
Si usas caracteres especiales, la URL se rompe y te tocará hacer una "traducción"
o codificación de la URL. Intenta usar contraseñas alfanuméricas seguras.

Error 3: Bad Request (400) al intentar abrir la página web
Causa: Django está bloqueando la URL generada por AWS por motivos de seguridad.
Solución:
Ir al archivo settings.py y agregar la URL (o IPs temporales) a los hosts permitidos:
ALLOWED_HOSTS = ["*", "172.31.8.32", "tu-url-de-aws.elasticbeanstalk.com"]
*Importante: Después de modificar esto en código, recuerda hacer `git add .`,
`git commit` y nuevamente `eb deploy` para subir los cambios.*

Error 4: Timeouts o imposibilidad de conectar a RDS
Causa: La base de datos en AWS RDS tiene bloqueadas las conexiones entrantes.
Solución:
Ir a la consola de AWS -> RDS -> Tu Base de Datos -> Security Groups.
Asegurarse de agregar una "Regla de Entrada" (Inbound Rule) para el protocolo
PostgreSQL permitiendo el acceso desde 0.0.0.0/0 (o idealmente solo desde la IP
de tu aplicación).
"""
