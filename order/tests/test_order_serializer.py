import pytest

from order.models import Order
from order.serializers import OrderSerializer
from order.factories import OrderFactory, UserFactory
from product.factories import ProductFactory


@pytest.mark.django_db
class TestOrderSerializer:
    def test_serialize_order(self):
        order = OrderFactory()

        serializer = OrderSerializer(order)
        data = serializer.data

        assert "product" in data
        assert "total" in data
        assert isinstance(data["product"], list)
        assert isinstance(data["total"], float) or isinstance(data["total"], int)

        expected_total = sum([product.price for product in order.product.all()])
        assert data["total"] == expected_total

    def test_serialize_order_with_multiple_products(self):
        product1 = ProductFactory(price=100)
        product2 = ProductFactory(price=200)

        user = UserFactory()
        order = Order.objects.create(user=user)
        order.product.add(product1, product2)

        serializer = OrderSerializer(order)
        data = serializer.data

        assert len(data["product"]) == 2
        assert data["total"] == 300

        product_titles = [p["title"] for p in data["product"]]
        assert product1.title in product_titles
        assert product2.title in product_titles

    def test_deserialize_order(self):
        product1 = ProductFactory()
        product2 = ProductFactory()
        user = UserFactory()

        product_data = [
            {
                "title": product1.title,
                "price": product1.price,
                "active": product1.active,
                "category": [],
            },
            {
                "title": product2.title,
                "price": product2.price,
                "active": product2.active,
                "category": [],
            },
        ]

        order_data = {
            "product": product_data,
        }

        serializer = OrderSerializer(data=order_data, context={"user": user})
        assert serializer.is_valid(), serializer.errors

        order = serializer.save()
        assert order.product.count() == 2
        assert product1.title in [p.title for p in order.product.all()]
        assert product2.title in [p.title for p in order.product.all()]
        assert order.user == user
