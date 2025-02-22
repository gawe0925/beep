from rest_framework import serializers, response
from .models import Customer, Product, Order

class CustomerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = self.context.get('request', None)
        user = request.user
        if user.is_staff:
            pass
        else:
            if request and request.method == 'POST':
                self.fields.pop('points', None)
                self.fields.pop('voucher', None)
                self.fields.pop('premium', None)
                self.fields.pop('premium_issued_date', None)

            elif request and request.method == 'PUT':
                self.fields.pop('points', None)
                self.fields.pop('voucher', None)
                self.fields.pop('premium', None)
                self.fields.pop('premium_issued_date', None)
            
            elif request and user.is_authenticated:
                self.fields.pop('premium', None)
                self.fields.pop('premium_issued_date', None)

    class Meta:
        model = Customer
        fields = ["id", "first_name", "last_name", "email", "password", 
                  "mobile", "address", "post_code", "points", "voucher", 
                  "premium", "premium_issued_date", ]

    def create(self, validated_data):
        if 'username' not in validated_data:
            validated_data['username'] = validated_data['email']
        return super().create(validated_data)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ["undefined_1", "undefined_2", "undefined_3", "undefined_4", 
                   "undefined_5", "undefined_6", "undefined_7", "undefined_8", 
                   "undefined_9", "undefined_10",]


class OrderSerializer(serializers.ModelSerializer):
    items_name = serializers.SerializerMethodField()
    # items_name = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')

    class Meta:
        model = Order
        fields = ["items_name", "first_name", "last_name",
                  "mobile", "address", "post_code", "order_canceled", "total_amount"]
        read_only_fields = ["order_status", ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = self.context.get('request', None)
        user = request.user

        if user.is_staff:
            pass
        elif user.is_authenticated and request.method == 'POST':
            self.fields.pop('total_amount', None)
            self.fields.pop('order_status', None)
            self.fields.pop('order_canceled', None)


    def get_items_name(self, obj):
        return obj.items.name if obj.items else None