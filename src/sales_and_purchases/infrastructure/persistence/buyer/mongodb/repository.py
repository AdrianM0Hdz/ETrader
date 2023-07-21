from pymongo.collection import Collection

from src.sales_and_purchases.domain.common.values import Name

from src.sales_and_purchases.domain.buyer import Buyer
from src.sales_and_purchases.domain.buyer.values import BuyerId
from src.sales_and_purchases.domain.buyer.repository import BuyerRepository


class MongoDBBuyerRepository(BuyerRepository):
    def __init__(self, buyer_collection: Collection):
        self.buyer_collection = buyer_collection

    def _buyer_already_exists(self, buyer: Buyer) -> bool:
        buyer_data = self.buyer_collection.find_one({"id": buyer.id.value})
        return buyer_data is not None

    def get(self, id: BuyerId) -> Buyer:
        data = self.buyer_collection.find_one({"id": id.value})
        if data is None:
            raise FileNotFoundError("There is no buyer with that id")
        return Buyer(BuyerId(data["id"]), Name(data["name"]))

    def add(self, item: Buyer):
        if self._buyer_already_exists(item):
            raise ValueError("Buyer with that id alreay exits in buyer_collection")
        self.buyer_collection.insert_one(
            {"id": item.id.value, "name": item.name.value, "purchases": []}
        )

    def commit(self, item: Buyer):
        if not self._buyer_already_exists(item):
            raise ValueError("Cannot update an item that does not exists")
        self.buyer_collection.update_one(
            {"id": item.id.value}, {"$set": {"name": item.name.value}}
        )

    def delete(self, item: Buyer):
        if not self._buyer_already_exists(item):
            raise ValueError("Cannot delete an item that does not exist")
        self.buyer_collection.delete_one({"id": item.id.value})
