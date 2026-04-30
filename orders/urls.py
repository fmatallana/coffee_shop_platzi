from django.urls import path

from .views import CreateOrderProductView, MyorderView, ProductOrderAPI

urlpatterns = [
    path("mi-orden", MyorderView.as_view(), name="my_order"),
    path("agregar-producto", CreateOrderProductView.as_view(), name="add_product"),
    path("api/", ProductOrderAPI.as_view(), name="create_order_api"),
]
