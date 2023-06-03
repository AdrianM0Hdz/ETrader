from typing import List

from ..common.aggregate_root import AggregateRoot
from ..common.values import Name, Description

from ..product.values import ProductId, Price
from ..product.product import Product

from ..purchase.purchase import Purchase
from ..purchase.values import PurchaseId

from .values import SellerId


class Seller(AggregateRoot[SellerId]):
    def __init__(self, id: SellerId, name: Name, description: Description):
        super().__init__(id)
        self.name = name
        self.description = description
        self.products: List[ProductId] = []
        self.buyer_purchases: List[PurchaseId] = []

    def publish_product(
        self, product_id: ProductId, name: Name, description: Description, price: Price
    ) -> Product:
        published_product = Product(product_id, name, description, price, self.id)
        self.products.append(published_product.id)
        return published_product

    def register_purchase(self, purchase: Purchase):
        assert purchase.product in self.products
        self.buyer_purchases.append(purchase.id)
