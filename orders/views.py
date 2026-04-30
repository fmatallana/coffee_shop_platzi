from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import OrderProductForm
from .models import Order
from .serializers import OrderSerializer


class MyorderView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "orders/my_order.html"
    context_object_name = "order"

    def get_object(self, query_set=None):
        return Order.objects.filter(is_active=True, user=self.request.user).first()


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


class ProductOrderAPI(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        order, _ = Order.objects.get_or_create(
            is_active=True,
            user=self.request.user,
        )  # cuando el usuario crea un OrderProduct, este necesita estar asociado a una Order, asi es como se hace

        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            order=order
        )  # asi se accede al objeto antes de guardarlo, nombre_del_campo=valor El campo en OrderProduct que guarda la relación con la orden se llama order. Y el valor que se asigna es la variable order que obtuviste con get_or_create.
        return Response(serializer.data)
