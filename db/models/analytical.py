from peewee import *
from peewee import create_model_tables

from db.base import AnalyticsModel


class Time(AnalyticsModel):
    date = DateField()
    hour = IntegerField()

    class Meta:
        indexes = (
            (('date', 'hour',), True),
        )


class Article(AnalyticsModel):
    name = CharField(max_length=255)
    type = CharField(max_length=255)
    color = CharField(max_length=255)
    size = CharField(max_length=255)
    lowest_price = DecimalField()
    highest_price = DecimalField()

    # class Meta:
    #    indexes = (
    #        (('type', 'color', 'size',), False),
    #    )


class Customer(AnalyticsModel):
    name = CharField(max_length=255)
    gender = CharField(max_length=1)
    age = SmallIntegerField()

    class Meta:
        indexes = (
            (('gender', 'age', 'name'), True),
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
