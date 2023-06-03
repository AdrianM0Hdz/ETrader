from typing import List

from ..common.aggregate_root import AggregateRoot
from ..common.values import Name, Description

from ..product.values import ProductId, Price
from ..product.product import Product

from ..purchase.purchase import Purchase
from ..purchase.values import PurchaseId

from .values import SellerId


class Seller(AggregateRoot[SellerId]):
    def __init__(
        self,
        id: SellerId,
        name: Name,
        description: Description,
        products: List[Product],
        buyer_purchases: List[Purchase],
    ):
        super().__init__(id)

        assert isinstance(name, Name)

        assert isinstance(description, Description)

        assert isinstance(products, list)
        for product in products:
            assert isinstance(product, Product)

        assert isinstance(buyer_purchases, list)
        for buyer_purchase in buyer_purchases:
            assert isinstance(buyer_purchase, Purchase)
            assert buyer_purchase.product in products

        self.name = name
        self.description = description
        self.products = products
        self.buyer_purchases = buyer_purchases

    def publish_product(
        self, product_id: ProductId, name: Name, description: Description, price: Price
    ) -> Product:
        published_product = Product(product_id, name, description, price, self.id)
        self.products.append(published_product)
        return published_product

    def register_purchase(self, purchase: Purchase):
        assert purchase.product in self.products
        self.buyer_purchases.append(purchase)
