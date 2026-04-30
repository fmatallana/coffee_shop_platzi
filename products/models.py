from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.TextField(max_length=200, verbose_name="nombre")
    # verbose_name permite escribir en cualquier idioma como queremos que el campo se vea para el usuario final y permite administrar los datos del modelo

    description = models.TextField(max_length=300, verbose_name="Descripción")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    avaliable = models.BooleanField(default=True, verbose_name="Disponible")
    photo = models.ImageField(
        upload_to="logos", null=True, blank=True, verbose_name="Foto"
    )
    date_creation = models.DateField(
        auto_now_add=True, verbose_name="Fecha de creacion"
    )

    def __str__(self):
        return self.name
