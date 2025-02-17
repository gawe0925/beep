from rest_framework import serializers
from .models import Customer, Product, Order

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = ["undefined_1", "undefined_2", "undefined_3", "undefined_4", 
                   "undefined_5", "undefined_6", "undefined_7", "undefined_8", 
                   "undefined_9", "undefined_10", "user"]

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ["undefined_1", "undefined_2", "undefined_3", "undefined_4", 
                   "undefined_5", "undefined_6", "undefined_7", "undefined_8", 
                   "undefined_9", "undefined_10",]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ["undefined_1", "undefined_2", "undefined_3", "undefined_4", 
                   "undefined_5", "undefined_6", "undefined_7", "undefined_8", 
                   "undefined_9", "undefined_10",]