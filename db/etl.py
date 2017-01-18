from peewee import fn

import db.models.operational as operational
import db.models.analytical as analytical


def transform_offers_to_analytic_articles():
    query = operational.Offer.select(operational.Offer,
                                     fn.Max(operational.Offer.price).alias('highest_price'),
                                     fn.Min(operational.Offer.price).alias('lowest_price')) \
                             .group_by(operational.Offer.article)

    page = 1

    while query.paginate(page, 50).count() > 0:

        for offer in query.paginate(page, 50):
            origin_article = offer.article.get()

            data = {
                "highest_price": offer.highest_price,
                "lowest_price": offer.lowest_price,
                "name": origin_article.name,
                "type": origin_article.type.name,
                "size": origin_article.size.name,
                "color": origin_article.color.name
            }

            target_article, created = analytical.Article.get_or_create(id=origin_article.id,
                                                                       defaults=data)

            import ipdb; ipdb.set_trace()
            if not created:
                target_article.update(**data).execute()

        page += 1
