import datetime

from peewee import *
from peewee import create_model_tables

from db.base import OperationalModel


db = SqliteDatabase('operational.db')


class Type(OperationalModel):
    name = CharField(max_length=255)

    def __repr__(self):
        return "<Type: {name}>".format(name=self.name)


class Size(OperationalModel):
    name = CharField(max_length=255)

    def __repr__(self):
        return "<Size: {name}>".format(name=self.name)


class Color(OperationalModel):
    name = CharField(max_length=255)

    def __repr__(self):
        return "<Color: {name}>".format(name=self.name)


class Article(OperationalModel):
    name = CharField(max_length=255)
    type = ForeignKeyField(Type)
    size = ForeignKeyField(Size)
    color = ForeignKeyField(Color)

    def __repr__(self):
        return "<Article: {name}: {type}, {color}, {size}>".format(name=self.name,
                                                                   type=self.type,
                                                                   color=self.color,
                                                                   size=self.size)


class Customer(OperationalModel):
    JMBG = CharField(max_length=13, primary_key=True)
    name = CharField(max_length=255)
    gender = CharField(max_length=1)
    age = SmallIntegerField()

    def __repr__(self):
        return "<Customer: {name}: {JMBG}, {gender}, {age}>".format(name=self.name,
                                                                    age=self.age,
                                                                    gender=self.gender,
                                                                    JMBG=self.JMBG)


class City(OperationalModel):
    name = CharField(max_length=255)

    def __repr__(self):
        return "<City: {name}>".format(name=self.name)


class District(OperationalModel):
    name = CharField(max_length=255)
    city = ForeignKeyField(City)

    def __repr__(self):
        return "<District: {name}, {city}>".format(name=self.name, city=self.city)


class Seller(OperationalModel):
    PIB = CharField(max_length=9, primary_key=True)
    name = CharField(max_length=255)
    street = CharField(max_length=255)
    number = CharField(max_length=10)
    district = ForeignKeyField(District)

    def __repr__(self):
        return "<Seller: {name} - {PIB}: {street}, {number}, {district}>".format(name=self.name,
                                                                                 PIB=self.PIB,
                                                                                 street=self.street,
                                                                                 number=self.number,
                                                                                 district=self.district)


class Offer(OperationalModel):
    article = ForeignKeyField(Article)
    seller = ForeignKeyField(Seller, to_field=Seller.PIB)
    price = DecimalField(decimal_places=2)
    created_at = DateTimeField(default=datetime.datetime.now)

    def __repr__(self):
        return "<Offer: {article} - {seller} @ {price} RSD, {created_at}>".format(article=self.article,
                                                                              seller=self.seller,
                                                                              price=self.price,
                                                                              created_at=self.created_at)


class Order(OperationalModel):
    OrderStatus = (
        ('CR', 'created',),
        ('RE', 'realized',),
        ('CN', 'cancelled'),
    )

    customer = ForeignKeyField(Customer, to_field=Customer.JMBG)
    created_at = DateTimeField(default=datetime.datetime.now)
    status = CharField(max_length=2, choices=OrderStatus)

    def __repr__(self):
        return "<Order: {customer} {offer} - {created_at}; {status}".format(customer=self.customer,
                                                                            offer=self.offer_order.get().offer,
                                                                            status=self.status,
                                                                            created_at=self.created_at)


class OfferOrder(OperationalModel):
    offer = ForeignKeyField(Offer, related_name='offer_order')
    order = ForeignKeyField(Order, related_name='offer_order')
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
