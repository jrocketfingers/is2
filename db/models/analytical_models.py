from peewee import *
from peewee import create_model_tables

from db.base import AnalyticsModel


class Time(AnalyticsModel):
    date = DateField()
    time = TimeField()

    class Meta:
        indexes = (
            (('date', 'time',), True),
        )


class Article(AnalyticsModel):
    type = CharField(max_length=255)
    color = CharField(max_length=255)
    size = CharField(max_length=255)
    lowest_price = DecimalField()
    highest_price = DecimalField()

    class Meta:
        indexes = (
            (('type', 'color', 'size',), True),
        )


class Customer(AnalyticsModel):
    gender = CharField(max_length=1)
    age = SmallIntegerField()

    class Meta:
        indexes = (
            (('gender', 'age',), True),
        )


class Seller(AnalyticsModel):
    district = CharField(max_length=255)
    city = CharField(max_length=255)

    class Meta:
        indexes = (
            (('district', 'city',), True),
        )


class OfferGroup(AnalyticsModel):
    number_of = IntegerField()

    time = ForeignKeyField(Time)
    seller = ForeignKeyField(Seller)
    article = ForeignKeyField(Article)


class OrderGroup(AnalyticsModel):
    number_of = IntegerField()
    total_value = DecimalField(decimal_places=2)

    time = ForeignKeyField(Time)
    customer = ForeignKeyField(Customer)
    seller = ForeignKeyField(Seller)
    article = ForeignKeyField(Article)


def main():
    create_model_tables([Time, Article, Customer, Seller, OfferGroup, OrderGroup])


if __name__ == "__main__":
    main()