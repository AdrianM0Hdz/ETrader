from dataclasses import dataclass
from uuid import uuid1

from domain.common.aggregate_root import AggregateRoot
from domain.common.values import Name, NameData, Description, DescriptionData
from .values import ProductId, Price, PriceData


@dataclass(frozen=True)
class ProductData:
    id: str
    name: NameData
    description: DescriptionData
    price: PriceData


class Product(AggregateRoot[ProductId]):
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
        id = ProductId(uuid1())
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

    def get_data(self) -> ProductData:
        return ProductData(
            id=self.id.value,
            name=self.name.get_data(),
            description=self.description.get_data(),
            price=self.price.get_data(),
        )