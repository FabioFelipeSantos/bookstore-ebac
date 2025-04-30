import factory

from django.contrib.auth.models import User

from order.models import Order
from product.factories import ProductFactory


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker("pystr_format", string_format=r"product_username-????")
    email = factory.Faker(
        "pystr_format", string_format=r"product_email-?????@email.com"
    )

    class Meta:
        model = User


class OrderFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    @factory.post_generation
    def product(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for product in extracted:
                self.product.add(product)
        else:
            self.product.add(ProductFactory())

    class Meta:
        model = Order
        skip_postgeneration_save = True
