import json
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse

from product.factories import CategoryFactory, ProductFactory
from order.factories import UserFactory, OrderFactory
from product.models import Product
from order.models import Order


class TestOrderViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.category = CategoryFactory(title="Tecnologia")
        self.product = ProductFactory(
            title="Mouse", price="56.99", category=[self.category]
        )
        self.order = OrderFactory(product=[self.product])

    def test_order(self):
        response = self.client.get(reverse("order-list", kwargs={"version": "v1"}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order_data = json.loads(response.content)[0]
        self.assertEqual(order_data["product"][0]["title"], self.product.title)
        self.assertEqual(order_data["product"][0]["price"], float(self.product.price))
        self.assertEqual(order_data["product"][0]["active"], self.product.active)
        self.assertEqual(
            order_data["product"][0]["category"][0]["title"],
            self.product.category.first().title,
        )

    def test_create_order(self):
        user = UserFactory()
        product = ProductFactory()
        data = json.dumps({"products_id": [product.id], "user": user.id})

        response = self.client.post(
            reverse("order-list", kwargs={"version": "v1"}),
            data=data,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_order = Order.objects.get(user=user)

        self.assertEqual(created_order.user.username, user.username)
        self.assertEqual(created_order.product.first().title, product.title)
        self.assertEqual(created_order.product.first().price, product.price)
