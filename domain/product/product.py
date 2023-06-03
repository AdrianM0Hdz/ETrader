from ..common.aggregate_root import AggregateRoot
from ..common.values import Name, Description
from ..seller.values import SellerId
from .values import ProductId, Price


class Product(AggregateRoot[ProductId]):
    def __init__(
        self,
        id: ProductId,
        name: Name,
        description: Description,
        price: Price,
        seller: SellerId,
    ):
        super().__init__(id)

        assert isinstance(name, Name)
        assert isinstance(description, Description)
        assert isinstance(price, Price)
        assert isinstance(seller, SellerId)

        self.name = name
        self.description = description
        self.seller = seller
        self.price = price
        self.seller = seller
