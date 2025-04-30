import pytest
from django.db.utils import IntegrityError

from product.models import Product, Category
from product.factories import ProductFactory, CategoryFactory


@pytest.mark.django_db
class TestCategoryModel:
    def test_create_category(self):
        category = CategoryFactory()
        assert category.id is not None
        assert category.title is not None
        assert category.slug is not None

        assert str(category) == category.title

    def test_category_unique_slug(self):
        category1 = CategoryFactory(slug="unique-slug")

        with pytest.raises(IntegrityError):
            CategoryFactory(slug="unique-slug")

    def test_update_category(self):
        category = CategoryFactory(title="Original Title")

        category.title = "Updated Title"
        category.save()

        updated = Category.objects.get(id=category.id)
        assert updated.title == "Updated Title"

    def test_delete_category(self):
        category = CategoryFactory()
        category_id = category.id

        category.delete()

        assert not Category.objects.filter(id=category_id).exists()


@pytest.mark.django_db
class TestProductModel:
    def test_create_product(self):
        product = ProductFactory()
        assert product.id is not None
        assert product.title is not None
        assert product.price is not None

        assert product.category.exists()

    def test_product_with_multiple_categories(self):
        category1 = CategoryFactory()
        category2 = CategoryFactory()
        category3 = CategoryFactory()

        product = ProductFactory()
        product.category.clear()
        product.category.add(category1, category2, category3)

        assert product.category.count() == 3
        categories = set(product.category.all())
        assert category1 in categories
        assert category2 in categories
        assert category3 in categories

    def test_update_product(self):
        product = ProductFactory(title="Original Product")

        product.title = "Updated Product"
        product.price = 999.99
        product.save()

        updated = Product.objects.get(id=product.id)
        assert updated.title == "Updated Product"
        assert updated.price == 999.99

    def test_delete_product(self):
        product = ProductFactory()
        product_id = product.id

        product.delete()

        assert not Product.objects.filter(id=product_id).exists()

    def test_delete_category_does_not_delete_product(self):
        category = CategoryFactory()
        product = ProductFactory()

        product.category.clear()
        product.category.add(category)

        product_id = product.id

        category.delete()

        assert Product.objects.filter(id=product_id).exists()
        assert not Product.objects.get(id=product_id).category.exists()
