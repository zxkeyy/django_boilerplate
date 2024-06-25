from django.urls import path
from .views import CategoryViewSet, OrderItemViewSet, OrderViewSet, ProductImageViewSet, ProductInventoryViewSet, ProductViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('categories', CategoryViewSet)
router.register('products', ProductViewSet)
router.register('product_images', ProductImageViewSet)
router.register('product_inventory', ProductInventoryViewSet)
router.register('orders', OrderViewSet)
router.register('order_items', OrderItemViewSet)


urlpatterns = router.urls