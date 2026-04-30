"""
============================================================================
CREAR Y CONFIGURAR VISTAS PARA AGREGAR PRODUCTOS A UNA ORDEN
============================================================================

CONCEPTOS FUNDAMENTALES
=======================

¿Qué es ModelForm?
R: Clase de Django que genera automáticamente un formulario a partir de un modelo existente.
   Evita redefinir los campos manualmente, tomándolos directamente del modelo.
   Se configura a través de una clase Meta interna donde se define el modelo y los campos a usar.

¿Qué es la clase Meta dentro de un ModelForm?
R: Clase interna obligatoria en ModelForm que define su comportamiento.
   - model: el modelo del que se tomarán los campos.
   - fields: lista de los campos del modelo que se mostrarán en el formulario.

¿Qué es form_valid?
R: Método que se ejecuta automáticamente cuando el formulario pasa todas las validaciones.
   Se sobreescribe cuando se necesita agregar lógica personalizada antes de guardar,
   como asignar campos que el usuario no llena directamente (orden, cantidad, usuario).

¿Qué es get_or_create?
R: Método del ORM de Django que busca un objeto con los parámetros dados.
   Si el objeto no existe, lo crea automáticamente.
   Retorna una tupla: (objeto, created) donde created es un booleano que indica
   si el objeto fue creado (True) o ya existía (False).

¿Por qué se usa _ en order, _ = Order.objects.get_or_create()?
R: get_or_create retorna 2 valores obligatoriamente.
   El _ es una convención de Python para indicar que ese valor existe
   pero no será usado en ninguna parte del código.

¿Qué es reverse_lazy?
R: Función que resuelve una URL por su nombre de forma diferida (lazy).
   Se usa en success_url porque en el momento en que la clase se define,
   las URLs todavía no han sido cargadas por Django.
   reverse_lazy("my_order") espera a que las URLs estén disponibles antes de resolverse.


PASO A PASO - AGREGAR PRODUCTOS A UNA ORDEN
============================================

Paso 1: Crear el formulario en orders/forms.py

from django.forms import ModelForm
from .models import OrderProduct

class OrderProductForm(ModelForm):
    class Meta:
        model = OrderProduct
        fields = ["product"]

¿Por qué fields solo incluye "product" y no "order" ni "quantity"?
R: Porque "order" y "quantity" no deben ser llenados por el usuario.
   Se asignan automáticamente dentro de form_valid:
   - quantity se fija en 1 por defecto.
   - order se obtiene o crea a partir del usuario autenticado.


Paso 2: Crear la vista en orders/views.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import OrderProductForm
from .models import Order

class CreateOrderProductView(LoginRequiredMixin, CreateView):
    template_name = "orders/create_order_product.html"
    form_class = OrderProductForm
    success_url = reverse_lazy("my_order")

    def form_valid(self, form):
        order, _ = Order.objects.get_or_create(
            is_active=True,
            user=self.request.user,
        )
        form.instance.order = order
        form.instance.quantity = 1
        form.save()
        return super().form_valid(form)


Paso 3: Registrar la URL en orders/urls.py

path("agregar-producto", CreateOrderProductView.as_view(), name="add_product"),


Paso 4: Agregar el formulario en el template product_list.html

<form action="{% url 'add_product' %}" class="mt-4" method="post">
    {% csrf_token %}
    <input type="hidden" name="product" value="{{ product.id }}">
    <button
        class="block w-full rounded-sm bg-yellow-400 p-4
               text-sm font-medium transition hover:scale-105"
    >
        Agregar pedido
    </button>
</form>

¿Por qué el input es de tipo hidden?
R: Porque el usuario no necesita ver ni modificar el id del producto.
   El formulario solo necesita ese dato para saber qué producto agregar a la orden,
   pero visualmente solo se muestra el botón.

¿Por qué se usa method="post" y no method="get"?
R: Porque la operación modifica datos en el servidor (crea un OrderProduct).
   Las operaciones que crean, modifican o eliminan datos siempre deben usar POST.

¿Por qué se usa {% csrf_token %}?
R: Para proteger el formulario contra ataques Cross-Site Request Forgery (CSRF).
   Django rechazará cualquier formulario POST que no incluya este token.
"""
