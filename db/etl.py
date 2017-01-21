from peewee import fn

import db.models.operational as operational
import db.models.analytical as analytical


def transform_orders_to_analytic_orders():
    # Create a typed list of possible aliases
    class Aliases:
        customer_name = 'customer_name'
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

    query = operational.Order.select(fn.SUM(operational.Offer.price).alias(Aliases.total_value),
                                     fn.COUNT(operational.Order.id).alias(Aliases.number_of),
                                     operational.Customer.name.alias(Aliases.customer_name),
                                     operational.Customer.age,
                                     operational.Customer.gender,
                                     operational.District.name.alias(Aliases.district),
                                     operational.City.name.alias(Aliases.city),
                                     operational.Article.name.alias(Aliases.article_name),
                                     operational.Type.name.alias(Aliases.type),
                                     operational.Size.name.alias(Aliases.size),
                                     operational.Color.name.alias(Aliases.color),
                                     fn.DATE(operational.Order.created_at).alias(Aliases.date),
                                     operational.Order.created_at.hour.alias(Aliases.hour),
                                     fn.MIN(operational.Offer.price).alias(Aliases.lowest_price),
                                     fn.MIN(operational.Offer.price).alias(Aliases.highest_price))\
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
        .group_by(operational.Customer.name,
                  operational.Customer.age,
                  operational.Customer.gender,
                  operational.District.name,
                  operational.City.name,
                  operational.Article.name,
                  operational.Article.type,
                  operational.Article.size,
                  operational.Article.color,
                  fn.DATE(operational.Order.created_at),
                  operational.Order.created_at.hour)\
        .dicts()

    page = 1

    while query.paginate(page, 50).count() > 0:

        for order in query.paginate(page, 50):
            article_data = {
                'name': order.pop(Aliases.article_name),
                'type': order.pop(Aliases.type),
                'color': order.pop(Aliases.color),
                'size': order.pop(Aliases.size),
                # TODO: decide what to do with those
                'lowest_price': order.pop(Aliases.lowest_price),
                'highest_price': order.pop(Aliases.highest_price)
            }
            article, created = analytical.Article.get_or_create(**article_data)
            order['article'] = article

            customer_data = {
                'name': order.pop(Aliases.customer_name),
                'age': order.pop('age'),
                'gender': order.pop('gender')
            }
            customer, created = analytical.Customer.get_or_create(**customer_data)
            order['customer'] = customer

            seller_data = {
                'city': order.pop(Aliases.city),
                'district': order.pop(Aliases.district)
            }
            seller, created = analytical.Seller.get_or_create(**seller_data)
            order['seller'] = seller

            time_data = {
                'date': order.pop(Aliases.date),
                'hour': order.pop(Aliases.hour)
            }
            time, created = analytical.Time.get_or_create(**time_data)
            order['time'] = time

            analytical.OrderGroup.create(**order)

        page += 1
