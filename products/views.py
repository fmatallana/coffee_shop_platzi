from django.urls import reverse_lazy
from django.views import generic
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import ProductForm
from .models import Product
from .serializers import ProductSerializer

# Create your views here.


class Productlistview(generic.ListView):
    template_name = "products/product_list.html"
    model = Product
    context_object_name = "product_list"


class ProductFormView(generic.FormView):
    template_name = "products/add_product.html"
    form_class = ProductForm
    success_url = reverse_lazy("list_product")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ProductListAPI(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductAddAPI(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
