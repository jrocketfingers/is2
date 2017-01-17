from peewee import *
from peewee import create_model_tables


class Time(Model):
    date = DateField()
    time = TimeField()

    class Meta:
        indexes = (
            (('date', 'time',), True),
        )


class Article(Model):
    type = CharField(max_length=255)
    color = CharField(max_length=255)
    size = CharField(max_length=255)
    lowest_price = DecimalField()
    highest_price = DecimalField()

    class Meta:
        indexes = (
            (('type', 'color', 'size',), True),
        )


class Customer(Model):
    gender = CharField(max_length=1)
    age = SmallIntegerField()

    class Meta:
        indexes = (
            (('gender', 'age',), True),
        )


class Seller(Model):
    district = CharField(max_length=255)
    city = CharField(max_length=255)

    class Meta:
        indexes = (
            (('district', 'city',), True),
        )


class OfferGroup(Model):
    number_of = IntegerField()

    time = ForeignKeyField(Time)
    seller = ForeignKeyField(Seller)
    article = ForeignKeyField(Article)


class OrderGroup(Model):
    number_of = IntegerField()
    total_value = DecimalField(decimal_places=2)

    time = ForeignKeyField(Time)
    customer = ForeignKeyField(Customer)
    seller = ForeignKeyField(Seller)
    article = ForeignKeyField(Article)


def main():
    db = SqliteDatabase('analytics.db')
    db.connect()
    db.create_tables([Time, Article, Customer, Seller, OfferGroup, OrderGroup])
    db.close()


if __name__ == "__main__":
    main()
