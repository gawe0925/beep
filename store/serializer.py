from rest_framework import serializers, response
from .models import Customer, Product, Order, OrderItem

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


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    class Meta:
        model = OrderItem
        # fields = ['order', 'product', 'product_name', 'quantity', 'price']
        exclude = ["order"]


class OrderSerializer(serializers.ModelSerializer):
    item_details = serializers.SerializerMethodField()
    products = OrderItemSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ["products", "first_name", "last_name", 
                  "mobile", "address", "post_code", "order_canceled", "item_details"]
        read_only_fields = ["order_status", "total_amount", ]
    
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

    def stock_check(self, items):
        count = 0
        list_len = len(items)
        for item in items:
            order_quantity = item['quantity']
            product_name = item['product'].name
            stock_amount = item['product'].amount

            if order_quantity > stock_amount:
                print(f"{product_name} is insufficient, stock_amount:{stock_amount}")
                item['quantity'] = stock_amount
                count += 1

        if count == list_len:
            raise serializers.ValidationError("Ordered products are currently out of stock")
        return items


    def create(self, validated_data):
        request = self.context.get('request', None)

        if request and request.user:
            validated_data['customer'] = request.user
        else:
            raise serializers.ValidationError("Customer is required")

        items_data = validated_data.pop('products', [])
        valid_items = self.stock_check(items_data)
        order = Order.objects.create(**validated_data)
        order.total_amount = 0
        order.save()

        accumulate_amount = 0
        # create relation between Order and OrderItem
        for item in valid_items:
            OrderItem.objects.create(order=order, **item)
            print(f'Created OrderItem - product_name:{item['product'].name}, quantity:{item['quantity']}')
            accumulate_amount += item['product'].price * item['quantity']

            # update stock
            if item['quantity'] > 0:
                product = Product.objects.get(id=item['product'].id)
                product.amount = product.amount - item['quantity']
                print(f"updated {product.name}'s stock number")
                product.save()

        # generate serial_number for order
        order.total_amount = accumulate_amount
        order.save()

        return order

    def get_item_details(self, obj):
        items = obj.items.all()
        return [{"name": item.name, "stream": item.stream} for item in items]