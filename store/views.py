from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAdminOrReadyOnly
from .models import Customer, Product, Order
from .serializer import CustomerSerializer, ProductSerializer, OrderSerializer


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def create(self, request):
        if self.action == "create":
            pass


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadyOnly]


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]