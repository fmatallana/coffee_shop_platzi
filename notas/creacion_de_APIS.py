"""
primero se instala el framework

pip install djangorestframework , agregar al requirements pip freeze > requirements.txt


en setting se agrega a installed apps, recordar que como reocomendacion es mejor agregarlas antes de nuestras apps y despues de las de django


se agrega esto al final del archivo

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ]
}

los serializers permiten llevar desde un modelo a json un todo el contenido que tiene


se crea el serializers.py dentro de productos y se agrega esto

ModelSerializer funciona parecido a un modelform se le pasa un modelo y los campos que queremos usar del modelo

from rest_framework.serializers import ModelSerializer

from .models import Product


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "price",
            "avaliable",
            "photo",
            "date_creation",
        ]

se debe crear una vista, el metodo get lo que hace es que cuando se acceda a la url se deben evolver los productos en un comando json, para decirle o indicarle al serializer que la query de producst es una lista se agrega esto many=True,Response(serializer.data) es la data configurada en formato json

authentication_classes = [] y permission_classes = [] son una clase de permisos


class ProductListAPI(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


dentro de las urls se agrega esta vista

path("api/", ProductListAPI.as_view(), name="list_product_api"),

"""
