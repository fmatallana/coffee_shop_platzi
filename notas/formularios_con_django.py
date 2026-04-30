"""
============================================================================
FORMULARIOS CON DJANGO
============================================================================

CONCEPTOS FUNDAMENTALES
=======================

¿Qué es un formulario en Django?
R: Una clase Python que define los campos y validaciones de un formulario HTML.
   Django se encarga de renderizarlo en el template y validar los datos enviados.
   Se recomienda crear un archivo forms.py exclusivo para los formularios de cada app.

¿Qué es cleaned_data?
R: Diccionario que Django genera automáticamente después de validar un formulario.
   Contiene los datos del formulario ya validados y convertidos al tipo correcto.
   Solo está disponible después de que el formulario pase todas las validaciones.

¿Qué es FormView?
R: Vista genérica de Django que maneja el ciclo completo de un formulario:
   - GET: muestra el formulario vacío.
   - POST válido: ejecuta form_valid y redirige a success_url.
   - POST inválido: vuelve a mostrar el formulario con los errores.

¿Qué es reverse_lazy?
R: Función que resuelve una URL por su nombre de forma diferida.
   Se usa en success_url porque las URLs aún no están cargadas
   cuando Django define la clase de la vista.

¿Qué es {{ form.as_p }}?
R: Método que renderiza cada campo del formulario envuelto en etiquetas <p>.
   Es la forma más simple de mostrar un formulario sin estilos personalizados.


PASO A PASO - CREAR UN FORMULARIO
===================================

Paso 1: Crear forms.py en la app

from django import forms
from .models import Product

class ProductForm(forms.Form):
    name = forms.CharField(max_length=200, label="Nombre")
    description = forms.CharField(max_length=300, label="descripcion")
    price = forms.DecimalField(max_digits=10, decimal_places=2, label="precio")
    avaliable = forms.BooleanField(initial=True, label="disponible", required=False)
    photo = forms.ImageField(label="foto", required=False)

    def save(self):
        Product.objects.create(
            name=self.cleaned_data["name"],
            description=self.cleaned_data["description"],
            price=self.cleaned_data["price"],
            avaliable=self.cleaned_data["avaliable"],
            photo=self.cleaned_data["photo"],
        )

¿Por qué se crea el método save() dentro del formulario?
R: Para encapsular la lógica de creación del objeto dentro del formulario.
   La vista solo llama a form.save() sin necesidad de conocer los detalles
   de cómo se crea el producto.


Paso 2: Crear la vista en products/views.py

from django.views import generic
from django.urls import reverse_lazy
from .forms import ProductForm

class ProductFormView(generic.FormView):
    template_name = "products/add_product.html"
    form_class = ProductForm
    success_url = reverse_lazy("list_product")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


Paso 3: Crear urls.py en la app y registrarla en las urls globales

# products/urls.py
urlpatterns = [
    path("agregar/", ProductFormView.as_view(), name="add_product"),
    path("listado/", ProductListView.as_view(), name="list_product"),
]

# urls globales
path("products/", include("products.urls")),


Paso 4: Crear el template add_product.html

<form action="{% url 'add_product' %}" method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">agregar</button>
</form>

¿Por qué se usa action="{% url 'add_product' %}" en lugar de escribir la URL directamente?
R: Para evitar hardcodear la URL en el template.
   Si la URL cambia en urls.py, el template se actualiza automáticamente
   sin necesidad de buscar y cambiar cada referencia manual.


VERIFICAR QUE EL FORMULARIO FUNCIONA
======================================

Abrir una shell de Django para inspeccionar los datos creados:

./manage.py shell

# Importar el modelo
from products.models import Product

# Ver el primer producto creado
Product.objects.first()

# Ver todos los campos del producto
Product.objects.first().__dict__
"""
