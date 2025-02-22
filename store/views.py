from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.core.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAdminOrReadyOnly
from .models import Customer, Product, Order
from .serializer import CustomerSerializer, ProductSerializer, OrderSerializer


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_queryset(self):
        user = self.request.user
        # permission control
        if user.is_staff:
            return Customer.objects.all()
        return Customer.objects.filter(id=user.id)

    def get_object(self):
        user = self.request.user
        obj = super().get_object()
        # permission control
        if not user.is_staff and obj != user:
            raise PermissionDenied('Access Denied')
        return obj

    def partial_update(self, request, *args, **kwargs):
        # fliter queryset with user's info
        instance = self.get_object()
        # partially update request data
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        # if update result is not valid, then raise error message 
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadyOnly]


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(customer=user)