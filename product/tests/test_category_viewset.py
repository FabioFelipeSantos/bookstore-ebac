import json
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse

from product.factories import CategoryFactory
from product.models import Category


class TestCategoryViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.category = CategoryFactory(title="Books")

    def test_get_all_category(self):
        response = self.client.get(reverse("category-list", kwargs={"version": "v1"}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        category_data = json.loads(response.content)

        self.assertEqual(category_data[0]["title"], self.category.title)

    def test_create_category(self):
        data = {"title": "Jogos", "slug": "jogos", "active": True}
        response = self.client.post(
            reverse("category-list", kwargs={"version": "v1"}),
            data=json.dumps(data),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_category = Category.objects.get(title="Jogos")

        self.assertEqual(created_category.title, "Jogos")
        self.assertEqual(created_category.slug, "jogos")
        self.assertEqual(created_category.active, True)
        self.assertGreater(created_category.id, 0)
