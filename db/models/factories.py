from peewee import fn

import factory
from factory_peewee import PeeweeModelFactory

from db.models import operational


class ArticleFactory(PeeweeModelFactory):
    class Meta:
        model = operational.Article

    type = factory.LazyFunction(lambda: operational.Type.select().order_by(fn.Random()).get())
    size = factory.LazyFunction(lambda: operational.Size.select().order_by(fn.Random()).get())
    color = factory.LazyFunction(lambda: operational.Color.select().order_by(fn.Random()).get())

    name = factory.Faker('bs')


class CustomerFactory(PeeweeModelFactory):
    class Meta:
        model = operational.Customer


class CityFactory(PeeweeModelFactory):
    class Meta:
        model = operational.City


class DistrictFactory(PeeweeModelFactory):
    class Meta:
        model = operational.District


class SellerFactory(PeeweeModelFactory):
    class Meta:
        model = operational.Seller


class OfferFactory(PeeweeModelFactory):
    class Meta:
        model = operational.Offer


class OrderFactory(PeeweeModelFactory):
    class Meta:
        model = operational.Order


class OfferOrderFactory(PeeweeModelFactory):
    class Meta:
        model = operational.OfferOrder
