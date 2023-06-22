from pymongo.collection import Collection


class BuyerQuerySet:
    def __init__(self, buyer_collection: Collection):
        self.buyer_collection = buyer_collection

    def find_one_by_id(self, id: str):
        return self.buyer_collection.find_one({"id": id})

    def find_one_by_name(self, name: str):
        return self.buyer_collection.find_one({"name": name})
