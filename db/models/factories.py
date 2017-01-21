from datetime import datetime
from random import randrange

import pytz
from dateutil.relativedelta import relativedelta
from peewee import fn

import factory
from factory.fuzzy import FuzzyText, FuzzyInteger, FuzzyDecimal, FuzzyDateTime, FuzzyChoice
from factory.faker import Faker
from factory_peewee import PeeweeModelFactory

from db.models import operational
from db.models.operational import Order, Offer, OfferOrder


class ArticleFactory(PeeweeModelFactory):
    class Meta:
        model = operational.Article

    type = factory.LazyFunction(lambda: operational.Type.select().order_by(fn.Rand()).get())
    size = factory.LazyFunction(lambda: operational.Size.select().order_by(fn.Rand()).get())
    color = factory.LazyFunction(lambda: operational.Color.select().order_by(fn.Rand()).get())

    name = factory.Faker('bs')


class CustomerFactory(PeeweeModelFactory):
    class Meta:
        model = operational.Customer

    JMBG = FuzzyText(chars="0123456789", length=13)
    name = Faker('name')
    gender = FuzzyText(chars="MF", length=1)
    age = FuzzyInteger(18, 100)


class CityFactory(PeeweeModelFactory):
    class Meta:
        model = operational.City

    name = Faker('city')


class DistrictFactory(PeeweeModelFactory):
    class Meta:
        model = operational.District

    name = Faker('bothify', text="## ??")
    city = factory.LazyFunction(lambda: operational.City.select().order_by(fn.Rand()).get())


class SellerFactory(PeeweeModelFactory):
    class Meta:
        model = operational.Seller

    PIB = FuzzyText(chars="0123456789", length=9)
    name = Faker('company')
    street = Faker('street_name')
    number = Faker('building_number')
    district = factory.LazyFunction(lambda: operational.District.select().order_by(fn.Rand()).get())


class OfferFactory(PeeweeModelFactory):
    class Meta:
        model = operational.Offer

    article = factory.LazyFunction(lambda: operational.Article.select().order_by(fn.Rand()).get())
    seller = factory.LazyFunction(lambda: operational.Seller.select().order_by(fn.Rand()).get())
    price = FuzzyDecimal(200, 50000)
    created_at = FuzzyDateTime(start_dt=(datetime.now(pytz.timezone('Europe/Belgrade')) - relativedelta(years=1)),
                               end_dt=datetime.now(pytz.timezone('Europe/Belgrade'))) #factory.Faker('date_time_this_year', before_now=True, after_now=False, tzinfo=None)


class OrderFactory(PeeweeModelFactory):
    class Meta:
        model = operational.Order

    customer = factory.LazyFunction(lambda: operational.Customer.select().order_by(fn.Rand()).get())
    created_at = FuzzyDateTime(start_dt=(datetime.now(pytz.timezone('Europe/Belgrade')) - relativedelta(years=1)),
                               end_dt=datetime.now(pytz.timezone('Europe/Belgrade'))) #factory.Faker('date_time_this_year', before_now=True, after_now=False, tzinfo=None)
    status = FuzzyChoice([status[0] for status in Order.OrderStatus])

    @factory.post_generation
    def articles(self, create, extracted, **kwargs):
        if not create:
            return

        n_offers = randrange(1, 5)

        offers = [offer for offer in Offer.select().order_by(fn.Rand()).limit(n_offers)]

        for i in range(n_offers):
            offer_order = OfferOrder()
            offer_order.order_id = self.id
            offer_order.offer = offers[i]
            offer_order.amount = randrange(1, 2)

            offer_order.save(force_insert=True)


@factory.use_strategy(factory.BUILD_STRATEGY)
class OfferOrderFactory(PeeweeModelFactory):
    class Meta:
        model = operational.OfferOrder

    amount = FuzzyInteger(1, 2)


def init_operational():
    CityFactory.create_batch(20)
    print("Cities created.")
    DistrictFactory.create_batch(150)
    print("Districts created.")
    ArticleFactory.create_batch(150)
    print("Articles created.")
    CustomerFactory.create_batch(200)
    print("Customers created.")
    SellerFactory.create_batch(50)
    print("Sellers created.")
    OfferFactory.create_batch(150)
    print("Offers created.")
    OrderFactory.create_batch(800)
    print("Orders created.")
