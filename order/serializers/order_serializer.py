from rest_framework import serializers
from django.contrib.auth.models import User

from order.models import Order
from product.models import Product, Category
from product.serializers import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(required=False, many=True, read_only=True)
    products_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True, many=True
    )
    total = serializers.SerializerMethodField()
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def get_total(self, instance):
        total = sum([product.price for product in instance.product.all()])
        return total

    def create(self, validated_data):
        products_id = validated_data.pop("products_id", [])
        user = validated_data.pop("user")

        order = Order.objects.create(user=user, **validated_data)

        if products_id:
            for product in products_id:
                order.product.add(product)

        return order

    def update(self, instance, validated_data):
        products_data = validated_data.pop("product", None)

        if products_data is not None:
            instance.product.clear()

            for product_data in products_data:
                categories_data = product_data.pop("category", [])

                product, _ = Product.objects.get_or_create(
                    title=product_data.get("title"), defaults=product_data
                )

                for category_data in categories_data:
                    category, _ = Category.objects.get_or_create(
                        slug=category_data.get("slug"), defaults=category_data
                    )
                    product.category.add(category)

                instance.product.add(product)

        return instance

    class Meta:
        model = Order
        fields = ["id", "product", "total", "user", "products_id"]
        extra_kwargs = {"product": {"required": False}}


class OrderSerializerV1(serializers.ModelSerializer):
    product = ProductSerializer(required=True, many=True)
    total = serializers.SerializerMethodField()

    def get_total(self, instance):
        total = sum([product.price for product in instance.product.all()])
        return total

    def create(self, validated_data):
        products_data = validated_data.pop("product")
        user = self.context.get("user")
        if not user:
            raise serializers.ValidationError(
                {"user": "Usuario obrigatório para criar um pedido"}
            )
        order = Order.objects.create(user=user, **validated_data)

        for product_data in products_data:
            categories_data = product_data.pop("category", [])
            product, _ = Product.objects.get_or_create(
                title=product_data.get("title"), defaults=product_data
            )

            for category_data in categories_data:
                category, _ = Category.objects.get_or_create(
                    slug=category_data.get("slug"), defaults=category_data
                )
                product.category.add(category)
            order.product.add(product)

        return order

    def update(self, instance, validated_data):
        products_data = validated_data.pop("product", None)

        if products_data is not None:
            instance.product.clear()

            for product_data in products_data:
                categories_data = product_data.pop("category", [])

                product, _ = Product.objects.get_or_create(
                    title=product_data.get("title"), defaults=product_data
                )

                for category_data in categories_data:
                    category, _ = Category.objects.get_or_create(
                        slug=category_data.get("slug"), defaults=category_data
                    )
                    product.category.add(category)

                instance.product.add(product)

        return instance

    class Meta:
        model = Order
        fields = ["product", "total"]
