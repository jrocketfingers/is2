from peewee import fn

import db.models.operational as operational
import db.models.analytical as analytical
from db.utils import peewee_get_kwargs


class Aliases:
    """Typed list of possible aliases"""
    customer_name = 'customer_name'
    seller_name = 'seller_name'
    seller_street = 'seller_street'
    seller_number = 'seller_number'
    article_name = 'article_name'
    total_value = 'total_value'
    number_of = 'number_of'
    district = 'district'
    city = 'city'
    type = 'type'
    size = 'size'
    color = 'color'
    date = 'date'
    hour = 'hour'
    lowest_price = 'lowest_price'
    highest_price = 'highest_price'


orders_query = operational.Order.select(fn.SUM(operational.Offer.price).alias(Aliases.total_value),
                                        fn.COUNT(operational.Order.id).alias(Aliases.number_of),
                                        operational.Customer.JMBG,
                                        operational.Customer.name.alias(Aliases.customer_name),
                                        operational.Customer.age,
                                        operational.Customer.gender,
                                        operational.Seller.PIB,
                                        operational.Seller.name.alias(Aliases.seller_name),
                                        operational.Seller.street.alias(Aliases.seller_street),
                                        operational.Seller.number.alias(Aliases.seller_number),
                                        operational.District.name.alias(Aliases.district),
                                        operational.City.name.alias(Aliases.city),
                                        operational.Article.name.alias(Aliases.article_name),
                                        operational.Type.name.alias(Aliases.type),
                                        operational.Size.name.alias(Aliases.size),
                                        operational.Color.name.alias(Aliases.color),
                                        fn.DATE(operational.Order.created_at).alias(Aliases.date),
                                        operational.Order.created_at.hour.alias(Aliases.hour),
                                        fn.MIN(operational.Offer.price).alias(Aliases.lowest_price),
                                        fn.MAX(operational.Offer.price).alias(Aliases.highest_price))\
        .join(operational.Customer)\
        .join(operational.OfferOrder, on=(operational.OfferOrder.order_id == operational.Order.id))\
        .join(operational.Offer)\
        .join(operational.Article)\
        .join(operational.Seller, on=(operational.Offer.seller_id == operational.Seller.PIB)) \
        .join(operational.District, on=(operational.Seller.district_id == operational.District.id))\
        .join(operational.City, on=(operational.District.city_id == operational.City.id))\
        .join(operational.Type, on=(operational.Type.id == operational.Article.type_id))\
        .join(operational.Color, on=(operational.Color.id == operational.Article.color_id))\
        .join(operational.Size, on=(operational.Size.id == operational.Article.size_id))\
        .group_by(operational.Customer.JMBG,
                  operational.Customer.name,
                  operational.Customer.gender,
                  operational.Customer.age,
                  operational.Seller.PIB,
                  operational.Seller.name,
                  operational.Seller.street,
                  operational.Seller.number,
                  operational.District.name,
                  operational.City.name,
                  operational.Article.id,
                  fn.DATE(operational.Order.created_at),
                  operational.Order.created_at.hour)


def transform_orders_to_analytic_orders():
    query = orders_query.dicts()

    page = 1

    while query.paginate(page, 50).count() > 0:

        for order in query.paginate(page, 50):
            # at this point, order contains all the data from the query
            # we're going to pop the 1st level join data, and all further joins, denormalized
            # just so we can create the dimension entries, and point towards the entries from the modified order (fact)

            time_data = {
                'date': order.pop(Aliases.date),
                'hour': order.pop(Aliases.hour)
            }
            time, created = analytical.Time.get_or_create(**time_data)
            order['time'] = time

            article_data = {
                'name': order.pop(Aliases.article_name),
                'type': order.pop(Aliases.type),
                'color': order.pop(Aliases.color),
                'size': order.pop(Aliases.size),
            }
            article, created = peewee_get_kwargs(analytical.Article, **article_data)
            order['article'] = article

            customer_data = {
                'JMBG': order.pop('JMBG'),
                'name': order.pop(Aliases.customer_name),
                'age': order.pop('age'),
                'gender': order.pop('gender')
            }
            customer, created = analytical.Customer.get_or_create(**customer_data)
            order['customer'] = customer

            seller_data = {
                'PIB': order.pop('PIB'),
                'name': order.pop(Aliases.seller_name),
                'street': order.pop(Aliases.seller_street),
                'number': order.pop(Aliases.seller_number),
                'city': order.pop(Aliases.city),
                'district': order.pop(Aliases.district)
            }
            seller, created = analytical.Seller.get_or_create(**seller_data)
            order['seller'] = seller

            analytical.OrderGroup.create(**order)

        page += 1


offers_query = operational.Offer.select(fn.COUNT(operational.Offer.id).alias(Aliases.number_of),
                                        operational.Seller.PIB,
                                        operational.Seller.name.alias(Aliases.seller_name),
                                        operational.Seller.street.alias(Aliases.seller_street),
                                        operational.Seller.number.alias(Aliases.seller_number),
                                        operational.District.name.alias(Aliases.district),
                                        operational.City.name.alias(Aliases.city),
                                        operational.Article.name.alias(Aliases.article_name),
                                        operational.Type.name.alias(Aliases.type),
                                        operational.Color.name.alias(Aliases.color),
                                        operational.Size.name.alias(Aliases.size),
                                        fn.DATE(operational.Offer.created_at).alias(Aliases.date)) \
    .join(operational.Seller, on=(operational.Seller.PIB == operational.Offer.seller_id)) \
    .join(operational.District, on=(operational.District.id == operational.Seller.district_id)) \
    .join(operational.City, on=(operational.City.id == operational.District.city_id)) \
    .join(operational.Article, on=(operational.Article.id == operational.Offer.article_id)) \
    .join(operational.Type, on=(operational.Type.id == operational.Article.type_id)) \
    .join(operational.Color, on=(operational.Color.id == operational.Article.color_id)) \
    .join(operational.Size, on=(operational.Size.id == operational.Article.size_id)) \
    .group_by(operational.Seller.PIB,
              operational.Article.id,
              fn.DATE(operational.Offer.created_at))


def transform_offers_to_analytic_offers():
    query = offers_query.dicts()


last_offer_date_query = operational.Offer.select(operational.Seller.PIB.alias('seller_id'),
                                                 operational.Article.id.alias('article_id'),
                                                 fn.MAX(operational.Offer.created_at).alias('created_at')) \
    .join(operational.Article) \
    .join(operational.Seller, on=(operational.Seller.PIB == operational.Offer.seller_id)) \
    .group_by(operational.Seller.PIB, operational.Article.id) \
    .alias('last_offer_date')


current_offers_query = operational.Offer.select(operational.Offer) \
    .join(last_offer_date_query, on=((operational.Offer.article_id == last_offer_date_query.c.article_id) &
                                     (operational.Offer.seller_id == last_offer_date_query.c.seller_id) &
                                     (operational.Offer.created_at == last_offer_date_query.c.created_at))) \
    .alias('current_offers_query')


articles_query = operational.Article.select(operational.Article.name,
                                            operational.Color.name.alias(Aliases.color),
                                            operational.Size.name.alias(Aliases.size),
                                            operational.Type.name.alias(Aliases.type),
                                            fn.MAX(current_offers_query.c.price).alias(Aliases.highest_price),
                                            fn.MIN(current_offers_query.c.price).alias(Aliases.lowest_price)) \
    .join(current_offers_query, on=(operational.Article.id == current_offers_query.c.article_id)) \
    .join(operational.Color, on=(operational.Article.color_id == operational.Color.id)) \
    .join(operational.Size, on=(operational.Article.size_id == operational.Size.id)) \
    .join(operational.Type, on=(operational.Article.type_id == operational.Type.id)) \
    .group_by(operational.Article.id)


def load_articles():
    query = articles_query.dicts()

    page = 1

    while query.paginate(page, 50).count() > 0:
        for article_data in query.paginate(page, 50):
            article = analytical.Article(**article_data)
            article.save()

        page += 1
