from peewee import *
from peewee import create_model_tables

from db.base import AnalyticsModel


class OrderTime(AnalyticsModel):
    date = DateField()
    hour = IntegerField()

    class Meta:
        indexes = (
            (('date', 'hour',), True),
        )


class OfferTime(AnalyticsModel):
    date = DateField()


class Article(AnalyticsModel):
    name = CharField(max_length=255)
    type = CharField(max_length=255)
    color = CharField(max_length=255)
    size = CharField(max_length=255)


class Customer(AnalyticsModel):
    JMBG = CharField(max_length=13, primary_key=True)
    name = CharField(max_length=255)
    gender = CharField(max_length=1)
    age = SmallIntegerField()


class Seller(AnalyticsModel):
    PIB = CharField(max_length=9, primary_key=True)
    name = CharField(max_length=255)
    street = CharField(max_length=255)
    number = CharField(max_length=10)
    district = CharField(max_length=255)
    city = CharField(max_length=255)


class Price(AnalyticsModel):
    value = DecimalField()


class OfferFact(AnalyticsModel):
    number_of = IntegerField()

    time = ForeignKeyField(OfferTime)
    seller = ForeignKeyField(Seller, to_field=Seller.PIB)
    article = ForeignKeyField(Article)
    price = ForeignKeyField(Price)


class OrderFact(AnalyticsModel):
    number_of = IntegerField()
    total_value = DecimalField(decimal_places=2)

    time = ForeignKeyField(OrderTime)
    customer = ForeignKeyField(Customer, to_field=Customer.JMBG)
    seller = ForeignKeyField(Seller, to_field=Seller.PIB)
    article = ForeignKeyField(Article)


def main():
    create_model_tables([OrderTime, OfferTime, Article, Customer, Seller, OfferFact, OrderFact])


if __name__ == "__main__":
    main()
