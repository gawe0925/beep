from rest_framework import serializers
from .models import Customer, Product, Order

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["user_name", "mobile", "address", "post_code", "points", "voucher", ]
        # exclude = ["undefined_1", "undefined_2", "undefined_3", "undefined_4", 
        #            "undefined_5", "undefined_6", "undefined_7", "undefined_8", 
        #            "undefined_9", "undefined_10", "user"]

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ["undefined_1", "undefined_2", "undefined_3", "undefined_4", 
                   "undefined_5", "undefined_6", "undefined_7", "undefined_8", 
                   "undefined_9", "undefined_10",]


class OrderSerializer(serializers.ModelSerializer):
    items_name = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["items_name", "first_name", "last_name", 
                  "mobile", "address", "post_code", "total_amount", "order_status", "order_canceled",]
        # exclude = ["undefined_1", "undefined_2", "undefined_3", "undefined_4", 
        #            "undefined_5", "undefined_6", "undefined_7", "undefined_8", 
        #            "undefined_9", "undefined_10",]

    def get_product_name(self, obj):
        return obj.items.name if obj.items else None