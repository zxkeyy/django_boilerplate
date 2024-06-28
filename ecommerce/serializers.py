from rest_framework import serializers

from .models import Category, Order, OrderItem, Product, ProductImage, ProductInventory

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description','parent', 'subcategories']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text']

class ProductInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInventory
        fields = ['id','product', 'quantity', 'updated_at']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    inventory = ProductInventorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'sku', 'images', 'inventory', 'created_at', 'updated_at']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id','order', 'product', 'quantity', 'price']
        read_only_fields = ['price', 'order']

    def create(self, validated_data):
        price = validated_data['product'].price
        validated_data['price'] = price
        return super().create(validated_data)

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'total', 'items', 'created_at', 'updated_at']
        read_only_fields = ['total', 'status']

    def create(self, validated_data):
        items = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        total = 0
        for item in items:
            total += item['product'].price * item['quantity']
            item['price'] = item['product'].price
            item['order'] = order
            OrderItem.objects.create(**item)
        order.total = total
        order.save()
        return order