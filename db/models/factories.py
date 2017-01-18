from peewee import fn

import factory
from factory.fuzzy import FuzzyText, FuzzyInteger, FuzzyDecimal
from factory.faker import Faker
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

    JMBG = FuzzyText(chars="0123456789", length=13)
    name = Faker('full_name')
    gender = FuzzyText(chars="MF")
    age = FuzzyInteger(18, 100)


class CityFactory(PeeweeModelFactory):
    class Meta:
        model = operational.City

    name = Faker('city')


class DistrictFactory(PeeweeModelFactory):
    class Meta:
        model = operational.District

    name = Faker('bothify', text="## ??")
    city = factory.LazyFunction(lambda: operational.City.select().order_by(fn.Random()).get())


class SellerFactory(PeeweeModelFactory):
    class Meta:
        model = operational.Seller

    PIB = FuzzyText(chars="0123456789", length=9)
    name = Faker('company')
    street = Faker('street_name')
    number = Faker('building_number')
    district = factory.LazyFunction(lambda: operational.District.select().order_by(fn.Random()).get())


class OfferFactory(PeeweeModelFactory):
    class Meta:
        model = operational.Offer

    article = factory.LazyFunction(lambda: operational.Article.select().order_by(fn.Random()).get())
    seller = factory.LazyFunction(lambda: operational.Seller.select().order_by(fn.Random()).get())
    price = FuzzyDecimal(0, 50000)
    created_at = factory.Faker('date_time_this_year', before_now=True, after_now=False, tzinfo=None)


class OrderFactory(PeeweeModelFactory):
    class Meta:
        model = operational.Order


class OfferOrderFactory(PeeweeModelFactory):
    class Meta:
        model = operational.OfferOrder
