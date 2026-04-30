from rest_framework.serializers import ModelSerializer

from .models import OrderProduct


class OrderSerializer(ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = [
            "product",
            "quantity",
        ]
