import datetime

from peewee import *
from peewee import create_model_tables

from db.base import OperationalModel


db = SqliteDatabase('operational.db')


class Type(OperationalModel):
    name = CharField(max_length=255)


class Size(OperationalModel):
    name = CharField(max_length=255)


class Color(OperationalModel):
    name = CharField(max_length=255)


class Article(OperationalModel):
    name = CharField(max_length=255)
    type = ForeignKeyField(Type)
    size = ForeignKeyField(Size)
    color = ForeignKeyField(Color)


class Customer(OperationalModel):
    JMBG = CharField(max_length=13, primary_key=True)
    name = CharField(max_length=255)
    gender = CharField(max_length=1)
    age = SmallIntegerField()


class City(OperationalModel):
    name = CharField(max_length=255)


class District(OperationalModel):
    name = CharField(max_length=255)
    city = ForeignKeyField(City)


class Seller(OperationalModel):
    PIB = CharField(max_length=9, primary_key=True)
    name = CharField(max_length=255)
    street = CharField(max_length=255)
    number = CharField(max_length=10)
    district = ForeignKeyField(District)


class Offer(OperationalModel):
    article = ForeignKeyField(Article)
    seller = ForeignKeyField(Seller)
    price = DecimalField(decimal_places=2)
    created_at = DateTimeField(default=datetime.datetime.now)


class Order(OperationalModel):
    OrderStatus = (
        ('CR', 'created',),
        ('RE', 'realized',),
        ('CN', 'cancelled'),
    )

    customer = ForeignKeyField(Customer)
    created_at = DateTimeField(default=datetime.datetime.now)
    status = CharField(max_length=1, choices=OrderStatus)


class OfferOrder(OperationalModel):
    offer = ForeignKeyField(Offer)
    order = ForeignKeyField(Order)
    amount = IntegerField()

    class Meta:
        primary_key = CompositeKey('offer', 'order')


def main():
    create_model_tables([Type, Color, Size, Article, Customer, City, District, Seller, Offer, Order, OfferOrder])

    Type(name="Pants").save()
    Type(name="Shirt").save()
    Type(name="Dress").save()
    Type(name="Jacket").save()
    Type(name="Suit").save()

    Color(name="Red").save()
    Color(name="Green").save()
    Color(name="Yellow").save()
    Color(name="Blue").save()

    Size(name="XXS").save()
    Size(name="S").save()
    Size(name="M").save()
    Size(name="L").save()
    Size(name="XL").save()
    Size(name="XXL").save()


if __name__ == "__main__":
    main()
