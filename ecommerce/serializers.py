from rest_framework import serializers

from .models import Category, Order, OrderItem, Product, ProductImage, ProductInventory

class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.StringRelatedField(many=True)

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
        fields = ['id', 'quantity', 'updated_at']

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    images = ProductImageSerializer(many=True, read_only=True)
    inventory = ProductInventorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'sku', 'images', 'inventory', 'created_at', 'updated_at']

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'total', 'status', 'items', 'created_at', 'updated_at']