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