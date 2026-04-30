"""
============================================================================
CONFIGURACIÓN DE LA APP DE PEDIDOS (ORDERS)
============================================================================

CONCEPTOS FUNDAMENTALES
=======================

¿Qué es la app orders?
R: Una aplicación Django encargada de gestionar los pedidos de café.
   Los clientes agregan productos a su orden y los meseros la visualizan desde el admin.

¿Qué es on_delete=models.CASCADE?
R: Comportamiento que se aplica cuando se elimina el objeto referenciado.
   Si se elimina un usuario, todas sus órdenes se eliminan también.
   Se usa en Order porque una orden sin usuario no tiene sentido.

¿Qué es on_delete=models.PROTECT?
R: Comportamiento que impide eliminar un objeto si tiene referencias activas.
   Se usa en OrderProduct.product para proteger la integridad de una orden ya creada.
   Si alguien intenta borrar un producto que está en una orden, Django lanzará un error.

¿Qué es auto_now_add en un campo de fecha?
R: Parámetro que llena automáticamente el campo con la fecha actual al momento de crear el objeto.
   Solo se escribe una vez, no se puede modificar después.
   Se usa en order_date para registrar cuándo se creó la orden.

¿Qué es is_active en el modelo Order?
R: Campo booleano que indica si la orden está siendo armada o ya fue enviada.
   True = el cliente todavía está agregando productos.
   False = la orden está lista y en espera de ser entregada.


PASO A PASO - CREAR LA APP DE PEDIDOS
======================================

Paso 1: Crear la app

./manage.py startapp orders


Paso 2: Registrar la app en settings.py

INSTALLED_APPS = [
    ...
    'orders',
]


Paso 3: Crear urls.py dentro de la app y registrarla en las urls globales

# urls globales
path("ordenes/", include("orders.urls")),


Paso 4: Crear los modelos

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    order_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"order {self.id} by {self.user}"


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.order} - {self.product}"

¿Por qué OrderProduct es un modelo separado?
R: Porque una orden puede tener múltiples productos.
   OrderProduct actúa como tabla intermedia que guarda cada ítem de la orden
   junto con su cantidad.


Paso 5: Crear y ejecutar las migraciones

./manage.py makemigrations
./manage.py migrate


Paso 6: Registrar los modelos en el admin

class OrderProductInLineAdmin(admin.TabularInline):
    model = OrderProduct
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    model = Order
    inlines = [OrderProductInLineAdmin]

admin.site.register(Order, OrderAdmin)

¿Qué es TabularInline?
R: Permite mostrar registros relacionados dentro del admin del modelo padre.
   En este caso, muestra los productos de una orden directamente dentro de la vista de Order.

¿Qué hace extra = 0?
R: Le indica al admin que no muestre filas vacías adicionales para crear nuevos registros.
   Solo muestra las filas con datos reales ya guardados.

¿Qué hace inlines = [OrderProductInLineAdmin]?
R: Le indica a OrderAdmin que muestre los OrderProduct relacionados
   dentro de la misma página de la orden en el admin.


BUENAS PRÁCTICAS
================

¿Qué hacer si necesito cambiar el nombre de un campo o una característica de un modelo?
R: Hacer el cambio directamente en models.py y luego correr makemigrations y migrate.
   Nunca editar manualmente el archivo de migración ya creado,
   ya que Django no detectará el cambio y la base de datos quedará desincronizada.


CONFIGURACIÓN DEL LOGOUT
=========================

¿Cómo configurar el logout en Django?
R: Requiere tres pasos: agregar la URL, configurar la redirección y agregar el botón en el HTML.

Paso 1: Agregar la URL en users/urls.py

path("logout/", LogoutView.as_view(), name="logout"),

Paso 2: Configurar la redirección después del logout en settings.py

LOGOUT_REDIRECT_URL = "login"

Paso 3: Agregar el formulario en el template

<form method="post" action="{% url 'logout' %}">
    {% csrf_token %}
    <button type="submit">Log Out</button>
</form>

¿Por qué el logout usa un formulario POST y no un enlace GET?
R: Porque el logout modifica el estado del servidor (destruye la sesión del usuario).
   Las operaciones que modifican datos siempre deben usar POST por seguridad.


¿Cómo mostrar el formulario de idioma en español?
R: Cambiar el parámetro LANGUAGE_CODE dentro de settings.py.

LANGUAGE_CODE = "es"
"""
