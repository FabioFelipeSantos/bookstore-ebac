from django.urls import path, include
from rest_framework import routers

from product.viewsets import ProductViewSet, CategoryViewSet

router = routers.SimpleRouter()
router.register(r"product", viewset=ProductViewSet, basename="product")
router.register(r"category", viewset=CategoryViewSet, basename="category")

urlpatterns = [path("", include(router.urls))]
