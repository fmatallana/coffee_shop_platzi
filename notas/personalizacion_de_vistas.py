"""
============================================================================
PERSONALIZACIÓN DE VISTAS - DETALLE DE ORDEN
============================================================================

CONCEPTOS FUNDAMENTALES
=======================

¿Qué es DetailView?
R: Vista genérica de Django que muestra un único objeto de un modelo.
   Recibe un identificador (normalmente el id) y retorna ese objeto al template.
   Documentación de vistas genéricas disponibles: ccbv.co.uk

¿Qué es context_object_name?
R: Parámetro que define el nombre con el que el objeto llegará al template.
   Sin este parámetro, Django envía el objeto con el nombre genérico "object".
   Al definirlo como "order", el template puede acceder con {{ order }} en lugar de {{ object }}.

¿Qué es get_object?
R: Método de DetailView que define qué objeto se va a mostrar.
   Se sobreescribe cuando se necesita una lógica personalizada para obtener el objeto,
   como filtrar por usuario activo en lugar de buscar por id en la URL.

¿Qué es LoginRequiredMixin?
R: Mixin que protege una vista para que solo usuarios autenticados puedan acceder.
   Si un usuario no está autenticado, lo redirige automáticamente a la URL de login.
   Siempre debe ir como primer parámetro en la definición de la clase.

¿Qué es LOGIN_URL en settings.py?
R: Variable que le indica a LoginRequiredMixin a qué URL redirigir
   cuando un usuario no autenticado intenta acceder a una vista protegida.

LOGIN_URL = "login"

¿Qué es orderproduct_set?
R: Manager inverso que Django crea automáticamente en las relaciones ForeignKey.
   Permite acceder a todos los OrderProduct relacionados con una Order específica.
   El patrón es: nombre_del_modelo_en_minúsculas + _set


PASO A PASO - CREAR LA VISTA DE MI ORDEN
==========================================

Paso 1: Crear la vista en orders/views.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

class MyOrderView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "orders/my_order.html"
    context_object_name = "order"

    def get_object(self, query_set=None):
        return Order.objects.filter(is_active=True, user=self.request.user).first()

¿Por qué se usa filter() en lugar de get() en get_object?
R: Porque get() lanza una excepción si no encuentra el objeto.
   filter().first() retorna None si no hay resultados, lo cual es más seguro
   cuando el usuario todavía no tiene una orden activa.


Paso 2: Registrar la URL en orders/urls.py

urlpatterns = [
    path("mi-orden", MyOrderView.as_view(), name="my_order")
]


Paso 3: Agregar LOGIN_URL en settings.py

LOGIN_URL = "login"


Paso 4: Crear el template orders/my_order.html

{% if user.is_authenticated and order.user == user %}
    {% for product_order in order.orderproduct_set.all %}
        {{ product_order.product.name }}
        {{ product_order.product.price }}
    {% empty %}
        No hay items en tu orden.
    {% endfor %}
{% else %}
    <p>No tienes permiso para ver esta orden o no has iniciado sesión.</p>
{% endif %}

¿Qué hace la etiqueta {% empty %}?
R: Se ejecuta cuando el bucle {% for %} no encuentra ningún elemento.
   Es equivalente a un if/else dentro del for, pero más limpio y legible.

¿Por qué se valida order.user == user en el template si ya usamos LoginRequiredMixin?
R: LoginRequiredMixin solo verifica que el usuario esté autenticado.
   La validación order.user == user es una capa extra de seguridad para asegurarse
   de que el usuario autenticado solo pueda ver su propia orden y no la de otros.
"""
