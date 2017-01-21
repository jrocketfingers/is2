SELECT customer.JMBG, seller.PIB, article.id as `article`, date(`order`.created_at), strftime("%H", `order`.created_at), COUNT(*) as `total` FROM `order`
INNER JOIN customer ON `order`.customer_id = customer.JMBG
INNER JOIN offerorder ON `order`.id = offerorder.order_id
INNER JOIN offer ON offerorder.offer_id = offer.id
INNER JOIN seller ON seller.PIB = offer.seller_id
INNER JOIN article ON offer.article_id = article.id
INNER JOIN type ON type.id = article.type_id
INNER JOIN color ON color.id = article.color_id
INNER JOIN `size` ON `size`.id = article.size_id
GROUP BY customer.JMBG, seller.PIB, article.id, date(`order`.created_at), strftime("%H", `order`.created_at)
ORDER BY total DESC;


SELECT Count(), Sum("t6"."price") FROM "order" AS t1
INNER JOIN "customer" AS t4 ON ("t1"."customer_id" = "t4"."JMBG")
INNER JOIN "offerorder" AS t5 ON ("t5"."order_id" = "t1"."id")
INNER JOIN "offer" AS t6 ON ("t5"."offer_id" = "t6"."id")
INNER JOIN "article" AS t2 ON ("t6"."article_id" = "t2"."id")
INNER JOIN "seller" AS t3 ON ("t6"."seller_id" = "t3"."PIB")
GROUP BY "t4"."JMBG", "t3"."PIB",
         "t2"."id", date_part("year", "t1"."created_at")

