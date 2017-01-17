import datetime

from peewee import *
from peewee import create_model_tables


class Type(Model):
    name = CharField(max_length=255)


class Size(Model):
    name = CharField(max_length=255)


class Color(Model):
    name = CharField(max_length=255)


class Article(Model):
    name = CharField(max_length=255)
    type = ForeignKeyField(Type)
    size = ForeignKeyField(Size)
    color = ForeignKeyField(Color)


class Customer(Model):
    JMBG = CharField(max_length=13, primary_key=True)
    name = CharField(max_length=255)
    gender = CharField(max_length=1)
    age = SmallIntegerField()


class City(Model):
    name = CharField(max_length=255)


class District(Model):
    name = CharField(max_length=255)
    city = ForeignKeyField(City)


class Seller(Model):
    PIB = CharField(max_length=9, primary_key=True)
    name = CharField(max_length=255)
    street = CharField(max_length=255)
    number = CharField(max_length=10)
    district = ForeignKeyField(District)


class Offer(Model):
    article = ForeignKeyField(Article)
    seller = ForeignKeyField(Seller)
    price = DecimalField(decimal_places=2)
    created_at = DateTimeField(default=datetime.datetime.now)


class Order(Model):
    OrderStatus = (
        ('CR', 'created',),
        ('RE', 'realized',),
        ('CN', 'cancelled'),
    )

    customer = ForeignKeyField(Customer)
    created_at = DateTimeField(default=datetime.datetime.now)
    status = CharField(max_length=1, choices=OrderStatus)


class OfferOrder(Model):
    offer = ForeignKeyField(Offer)
    order = ForeignKeyField(Order)
    amount = IntegerField()

    class Meta:
        primary_key = CompositeKey('offer', 'order')


def main():
    db = SqliteDatabase('operational.db')
    db.connect()
    db.create_tables([Type, Color, Size, Article, Customer, City, District, Seller, Offer, Order, OfferOrder])
    db.close()


if __name__ == "__main__":
    main()
