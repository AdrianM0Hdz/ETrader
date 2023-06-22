from pymongo.collection import Collection

from src.domain.buyer import Buyer
from src.domain.buyer.buyer import BuyerData
from src.domain.buyer.values import BuyerId
from src.domain.buyer.repository import BuyerRepository

from .data_model import (
    make_data_model_from_domain_model,
    make_domain_model_from_data_model,
)


class MongoDBBuyerRepository(BuyerRepository):
    def __init__(self, buyer_collection: Collection):
        self.buyer_collection = buyer_collection

    def _buyer_already_exists(self, buyer: BuyerData) -> bool:
        buyer_data = self.buyer_collection.find_one({"id": buyer.id.value})
        return buyer_data is not None

    def get(self, id: BuyerId) -> Buyer:
        data = self.buyer_collection.find_one({"id": id.value})
        if data is None:
            raise FileNotFoundError("There is no buyer with that id")
        return Buyer(data["id"], data["name"])

    def add(self, item: BuyerData):
        if self._buyer_already_exists(item):
            raise ValueError("Buyer with that id alreay exits in buyer_collection")
        data_item = make_data_model_from_domain_model(item)
        self.buyer_collection.insert_one(data_item)

    def commit(self, item: BuyerData):
        if not self._buyer_already_exists(item):
            raise ValueError("Cannot update an item that does not exists")

    def delete(self, item: BuyerData):
        if not self._buyer_already_exists(item):
            raise ValueError("Cannot delete an item that does not exist")
        self.buyer_collection.delete_one({"id": item.id.value})
