from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAdminOrReadyOnly
from .models import Customer, Product, Order
from .serializer import CustomerSerializer, ProductSerializer, OrderSerializer


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def update(self, instance, validated_date):
        if not self.context['request'].urse.is_staff:
            validated_date.pop('points', None)
            validated_date.pop('voucher', None)

            return super().update(instance, validated_date)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadyOnly]


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]