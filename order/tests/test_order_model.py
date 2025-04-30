import pytest
from django.contrib.auth.models import User
from order.models import Order
from order.factories import OrderFactory, UserFactory
from product.factories import ProductFactory


@pytest.mark.django_db
class TestOrderModel:
    def test_create_order(self):
        order = OrderFactory()
        assert order.id is not None
        assert order.user is not None
        assert order.product.exists()

    def test_create_order_with_multiple_products(self):
        product1 = ProductFactory()
        product2 = ProductFactory()
        product3 = ProductFactory()

        user = UserFactory()

        order = Order.objects.create(user=user)
        order.product.add(product1, product2, product3)

        assert order.product.count() == 3
        assert set(order.product.all()) == {product1, product2, product3}

    def test_order_user_relationship(self):
        user = UserFactory()
        order = OrderFactory(user=user)

        assert order.user == user
        assert order.user.username == user.username
        assert order.user.email == user.email

    def test_order_product_relationship(self):
        product = ProductFactory()
        order = OrderFactory()

        order.product.clear()
        order.product.add(product)

        assert order.product.count() == 1
        assert order.product.first() == product

    def test_delete_user_cascades_to_order(self):
        order = OrderFactory()
        user_id = order.user.id
        order_id = order.id

        User.objects.get(id=user_id).delete()

        assert not Order.objects.filter(id=order_id).exists()
