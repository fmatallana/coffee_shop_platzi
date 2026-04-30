"""
el testing es importante por que ayuda a validar que con un cambio que se haga se demuestra que con un cambio hecho se logra agregar funcionalidades y no dañar el codigo existente

test de listar los productos

los test deben ser creados en el archivo test.py de cada app

from django.test import TestCase
from django.urls import reverse

from .models import Product

este test sirve para verificar que la pagina cargue correctamente
se busca la url, en este caso es list_product
self.client es una funcionalidad clienet es un cliente http con el que se pueden hacer peticiones get post etc
esto debe guardarse en un response este response es el que ayuda a validar cual fue la respuesta al hacer la peticion, en este caso get


self.assert existen muchos tipos de assert pero en pocas palabras para lo que sirven los assers es para validar que el resultado esperado es igual al assert


para correr los test se debe hacer ./manage.py test

esto lo que hace es crear una DB de prueba dentro de la db del proyecto y despues de crearla corre las lineas del test

python permite hacer breackpoint() para hacer debugs

cuando la ejecucion llegue a breackpoint() lo que pasara es que en la consola saldra (pdb) que permitira ejecutara codigo python

esta es otra prueba self.assertEqual(response.context["products"].count(), 0) que varida que esponse.context["products"] sea igual a cero y sera correcto ya que no se ha creado ningun producto

en el test de abajo self.assertEqual(response.context["products"].count(), 1)

como con Product.objects.create si se creo un producto y se le pone un 1 ya que valida la cantidad de objetos que hay en response.context["products"] tambien sera exitoso este test
class ProductlistviewTest(TestCase):
    def test_should_return_200(self):
        url = reverse("list_product")
        response = self.client.get(url)
        breackpoint()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["products"].count(), 0)

    def test_should_return_200_whit_product(self):
        url = reverse("list_product")
        Product.objects.create(
            name="test", description="test", price="5", avaliable=True
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["products"].count(), 1)


TEST APP MY ORDER

se sigue el mismo proceso que en el test del cargue de la pagina pero en este caso se crea un usuario de la siguiente manera

get_user_model sirve para obtener el modelo del usuario

user = get_user_model().objects.create(username="test")
self.client.force_login(user)

force_login(user) se usa para no pasarle una contraseña

lass MyorderViewTest(TestCase):
    def test_no_loged_used_should_redirect(self):
        url = reverse("my_order")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/usuarios/login/?next=/pedidos/mi-orden")

    def test_loged_used_should_redirect(self):
        url = reverse("my_order")
        user = get_user_model().objects.create(username="test")
        self.client.force_login(user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

"""
