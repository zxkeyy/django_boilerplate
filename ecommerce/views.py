from django.shortcuts import render
from rest_framework import viewsets, permissions

from .permissions import IsAdminOrReadOnly
from .models import Category, Order, OrderItem, Product, ProductImage, ProductInventory
from .serializers import CategorySerializer, OrderItemSerializer, OrderSerializer, ProductImageSerializer, ProductInventorySerializer, ProductSerializer

# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminOrReadOnly]

class ProductInventoryViewSet(viewsets.ModelViewSet):
    queryset = ProductInventory.objects.all()
    serializer_class = ProductInventorySerializer
    permission_classes = [IsAdminOrReadOnly]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        This view should return a list of all the orders
        for the currently authenticated user.
        """
        user = self.request.user
        if user.is_authenticated:
            return Order.objects.filter(user=user)
        return Order.objects.none()  # Return an empty queryset for unauthenticated users

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ['get']

    def get_queryset(self):
        """
        This view should return a list of all the order items
        that are part of orders for the currently authenticated user.
        """
        user = self.request.user
        if user.is_authenticated:
            return OrderItem.objects.filter(order__user=user)
        return OrderItem.objects.none()  # Return an empty queryset for unauthenticated users