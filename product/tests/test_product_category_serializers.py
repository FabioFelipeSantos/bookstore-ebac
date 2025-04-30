import pytest
import uuid

from product.serializers import CategorySerializer, ProductSerializer
from product.factories import ProductFactory, CategoryFactory


@pytest.mark.django_db
class TestCategorySerializer:
    def test_serialize_category(self):
        category = CategoryFactory(
            title="Eletrônicos",
            slug="eletronicos",
            description="Produtos eletrônicos diversos",
            active=True,
        )

        serializer = CategorySerializer(category)
        data = serializer.data

        assert data["title"] == "Eletrônicos"
        assert data["slug"] == "eletronicos"
        assert data["description"] == "Produtos eletrônicos diversos"
        assert data["active"] == True

    def test_deserialize_valid_category(self):
        category_data = {
            "title": "Livros",
            "slug": "livros",
            "description": "Todos os tipos de livros",
            "active": True,
        }

        serializer = CategorySerializer(data=category_data)
        assert serializer.is_valid(), serializer.errors

        category = serializer.save()
        assert category.title == "Livros"
        assert category.slug == "livros"

    def test_deserialize_invalid_category_duplicate_slug(self):
        CategoryFactory(slug="unique-slug")

        category_data = {
            "title": "Nova Categoria",
            "slug": "unique-slug",
            "description": "Descrição",
            "active": True,
        }

        serializer = CategorySerializer(data=category_data)
        assert not serializer.is_valid()
        assert "slug" in serializer.errors


@pytest.mark.django_db
class TestProductSerializer:
    def test_serialize_product(self):
        category1 = CategoryFactory(title="Eletrônicos")
        category2 = CategoryFactory(title="Gadgets")

        product = ProductFactory(
            title="Smartphone",
            description="Um smartphone incrível",
            price=1299.99,
            active=True,
        )
        product.category.clear()
        product.category.add(category1, category2)

        serializer = ProductSerializer(product)
        data = serializer.data

        assert data["title"] == "Smartphone"
        assert data["description"] == "Um smartphone incrível"
        assert data["price"] == 1299.99
        assert data["active"] == True

        assert len(data["category"]) == 2
        category_titles = [c["title"] for c in data["category"]]
        assert "Eletrônicos" in category_titles
        assert "Gadgets" in category_titles

    def test_deserialize_simple_product(self):
        category1 = CategoryFactory()
        category2 = CategoryFactory()

        product_data = {
            "title": "Novo Produto",
            "description": "Descrição do novo produto",
            "price": 799.50,
            "active": True,
            "category": [
                {
                    "title": category1.title,
                    "slug": "categoria-teste-1-" + str(uuid.uuid4())[:8],
                    "description": category1.description,
                    "active": category1.active,
                },
                {
                    "title": category2.title,
                    "slug": "categoria-teste-2-" + str(uuid.uuid4())[:8],
                    "description": category2.description,
                    "active": category2.active,
                },
            ],
        }

        serializer = ProductSerializer(data=product_data)

        assert serializer.is_valid(), serializer.errors
        product = serializer.save()

        assert product.title == "Novo Produto"
        assert product.price == 799.50
        assert product.category.count() == 2
        assert category1.title in [c.title for c in product.category.all()]
        assert category2.title in [c.title for c in product.category.all()]
