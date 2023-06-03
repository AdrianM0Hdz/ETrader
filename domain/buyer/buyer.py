from typing import List
from uuid import uuid1

from ..common.aggregate_root import AggregateRoot
from ..common.values import Name

from ..purchase.purchase import Purchase
from ..purchase.values import PurchaseId, Quantity
from ..purchase.enums import PurchaseStatus

from ..product.product import Product

from ..seller.seller import Seller

from .values import BuyerId


class Buyer(AggregateRoot[BuyerId]):
    def __init__(self, id: BuyerId, name: Name, purchases: List[PurchaseId]):
        super().__init__(id)
        assert isinstance(name, Name)
        self.name = name
        self.purchases = purchases

    def purchase_product(
        self, product: Product, seller: Seller, quantity: Quantity
    ) -> Purchase:
        new_purchase = Purchase(
            PurchaseId(str(uuid1())),
            self,
            product,
            quantity,
            PurchaseStatus.TO_BE_DELIVERED,
        )
        self.purchases.append(new_purchase.id)
        seller.register_purchase(new_purchase)
        return new_purchase
