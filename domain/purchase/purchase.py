from ..common.aggregate_root import AggregateRoot

from ..buyer import Buyer
from ..buyer.values import BuyerId

from ..seller.values import SellerId

from ..product.values import ProductId
from ..product.product import Product

from .values import PurchaseId, Quantity

from .enums import PurchaseStatus


class Purchase(AggregateRoot[PurchaseId]):
    def __init__(
        self,
        id: PurchaseId,
        buyer: Buyer,
        product: Product,
        quantity: Quantity,
        status: PurchaseStatus,
    ):
        super().__init__(id)

        assert isinstance(buyer, Buyer)
        assert isinstance(id, PurchaseId)
        assert isinstance(product, ProductId)
        assert isinstance(quantity, Quantity)

        self.buyer = buyer
        self.product = product.id
        self.seller = product.seller
        self.quantity = quantity
        self.status = status
