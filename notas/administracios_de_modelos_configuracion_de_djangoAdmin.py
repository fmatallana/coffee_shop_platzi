"""
django viene con un admin de manera interna

esto nos ayuda a administrar los modelos desde un admin web


para acceder a el se hacer ./manage.py runserver y en la url se agrega /admin


este admin nos devuelve un login

existe un comando para crear un super usuario, es decir un usuario que pueda acceder al admin

./manage.py createsuperuser

matallana
1076737320#Fm


djago viene con un sistema de autenticacion incluido, al darle clck en users se puede ver el super usuario que se creo

registro de modelos dentro del admin

dentro de admin.py se agrega lo siguiente

class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ["name", "price", "date_creation"]
    search_fields = ["name"]


admin.site.register(Product, ProductAdmin)

ModelAdmin permite crear o registrar modelos en el admin

se le pasa el modelo dentro de la variable model y se importa

agregacion de campos dentro de admin

list_display = ["name", "price", "date_creation"]


buscadores

search_fields = ["name"]


esta linea se usa para terminar de crear los usuarios

admin.site.register(Product, ProductAdmin)

pide el modelo y el nombre de la clase

si por alguna casualidad desde el admin se agrega una imagen y al ir a la url de donde se espera ver la imagen no sale, se soluciona con lo siguente  dentro de urls.pty

from django.conf.urls.static import static
from django.conf import settings


+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



"""
