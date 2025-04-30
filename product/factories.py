import factory

from product.models import Product, Category


class CategoryFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("pystr_format", string_format=r"category_title-?????")
    slug = factory.Faker("pystr_format", string_format=r"category_slug-?????")
    description = factory.Faker(
        "pystr_format", string_format=r"category_description-?????"
    )
    active = factory.Iterator([True, False])

    class Meta:
        model = Category
        skip_postgeneration_save = True


class ProductFactory(factory.django.DjangoModelFactory):
    price = factory.Faker("pyfloat", positive=True, min_value=400, max_value=1500)
    title = factory.Faker("pystr_format", string_format=r"product_title-?????")

    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for category in extracted:
                self.category.add(category)
        else:
            self.category.add(CategoryFactory())

    class Meta:
        model = Product
        skip_postgeneration_save = True
