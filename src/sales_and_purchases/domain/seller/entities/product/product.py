from uuid import uuid1

from src.shared_kernel.domain.entity import Entity
from src.sales_and_purchases.domain.common.values import Name, Description
from .values import ProductId, Price


class Product(Entity[ProductId]):
    def __init__(
        self,
        id: ProductId,
        name: Name,
        description: Description,
        price: Price,
    ):
        super().__init__(id)

        assert isinstance(name, Name)
        assert isinstance(description, Description)
        assert isinstance(price, Price)

        self.__name = name
        self.__description = description
        self.__price = price

    @classmethod
    def create_new(
        cls, name: Name, descriptioin: Description, price: Price
    ) -> "Product":
        id = ProductId(str(uuid1()))
        return cls(id, name, descriptioin, price)

    @property
    def name(self) -> Name:
        return self.__name

    @name.setter
    def name(self, new_name: Name):
        assert isinstance(new_name, Name)
        self.__name = new_name

    @property
    def description(self) -> Description:
        return self.__description

    @description.setter
    def description(self, new_description: Description):
        assert isinstance(new_description, Description)
        self.__description = new_description

    @property
    def price(self) -> Price:
        return self.__price

    @price.setter
    def price(self, new_price: Price):
        assert isinstance(new_price, Price)
        self.__price = new_price
