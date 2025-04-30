from rest_framework import serializers

from product.models import Product, Category
from .category_serializer import CategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=True, many=True)

    def create(self, validated_data):
        categories_data = validated_data.pop("category")

        product = Product.objects.create(**validated_data)

        for category_data in categories_data:
            category, _ = Category.objects.get_or_create(
                slug=category_data.get("slug"), defaults=category_data
            )
            product.category.add(category)

        return product

    def update(self, instance, validated_data):
        categories_data = validated_data.pop("category", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if categories_data is not None:
            instance.category.clear()
            for category_data in categories_data:
                category, _ = Category.objects.get_or_create(
                    slug=category_data.get("slug"), defaults=category_data
                )
            instance.category.add(category)
        return instance

    class Meta:
        model = Product
        fields = ["title", "description", "price", "active", "category"]
