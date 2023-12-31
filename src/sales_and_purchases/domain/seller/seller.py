from dataclasses import dataclass
from typing import Dict, List, Tuple
from uuid import uuid1

from src.shared_kernel.domain.aggregate_root import AggregateRoot
from ..common.values import Name, NameData, Description, DescriptionData

from ..buyer.values import BuyerId

from .entities.product.values import ProductId, Price
from .entities.product.product import Product

from .entities.purchase.purchase import Purchase
from .entities.purchase.values import PurchaseId, Quantity
from .entities.purchase.enums import PurchaseStatus

from .values import SellerId


class Seller(AggregateRoot[SellerId]):
    def __init__(
        self,
        id: SellerId,
        name: Name,
        description: Description,
        products: Dict[Product, List[Purchase]],
    ):
        assert isinstance(id, SellerId)
        super().__init__(id)

        assert isinstance(name, Name)
        assert isinstance(description, Description)
        assert isinstance(products, dict)
        for product, purchases in products.items():
            assert isinstance(product, Product)
            assert isinstance(purchases, list)
            for purchase in purchases:
                assert isinstance(purchase, Purchase)
        self.__name = name
        self.__description = description
        self.__products = products

    @classmethod
    def create_new(cls, name: Name, description: Description) -> "Seller":
        id = SellerId(str(uuid1()))
        return cls(id, name, description, {})

    @property
    def name(self) -> Name:
        return self.__name

    @name.setter
    def name(self, new_name: Name):
        assert isinstance(new_name, Name)
        self.name = new_name

    @property
    def description(self) -> Description:
        return self.__description

    @description.setter
    def description(self, new_description: Description):
        assert isinstance(new_description, Description)
        self.description = new_description

    @property
    def products(self) -> Tuple[Product]:
        return tuple(self.__products.keys())

    def get_purchases_of_product(self, product: Product) -> List[Purchase]:
        purchases = self.__products.get(product)
        if purchases is None:
            raise ValueError("Seller does not set such product")
        return purchases

    def register_product(
        self, product_name: Name, product_description: Description, product_price: Price
    ):
        published_product = Product.create_new(
            product_name, product_description, product_price
        )
        self.__products[published_product] = []

    def register_purchase(
        self, product_id: ProductId, buyer_id: BuyerId, quantity: Quantity
    ):
        for product in self.__products:
            if product.id == product_id:
                new_purchase = Purchase.create_new(buyer_id, quantity)
                self.__products[product].append(new_purchase)
                return
        raise BaseException("Seller does not offer product with that id")

    def _get_purchase(self, product_id: ProductId, purchase_id: PurchaseId) -> Purchase:
        for product, purchases in self.__products.items():
            if product.id == product_id:
                indx = -1
                try:
                    for i, purchase in enumerate(purchases):
                        if purchase.id == purchase_id:
                            indx = i
                            break
                except ValueError:
                    raise BaseException(
                        "Purchase with that id does not exist for product with that id"
                    )
                return purchases[indx]
        raise BaseException(
            "Product with that id does not exist within the products of the seller"
        )

    def mark_purchase_delivered(self, product_id: ProductId, purchase_id: PurchaseId):
        purchase = self._get_purchase(product_id, purchase_id)
        purchase.status = PurchaseStatus.DELIVERED

    def mark_purchase_canceled(self, product_id: ProductId, purchase_id: PurchaseId):
        purchase = self._get_purchase(product_id, purchase_id)
        purchase.status = PurchaseStatus.CANCELED
