from domain.common.values import Name
from .....domain.buyer import Buyer
from .....domain.buyer.values import BuyerId
from .....domain.buyer.repository import BuyerRepository


class MockBuyerRepository(BuyerRepository):
    def __init__(self):
        self.data = []

    def add(self, item: Buyer):
        self.data.append(item)

    def get(self, id: BuyerId):
        for user in self.data:
            if user.id == id:
                return user
        return None

    def get_by_name(self, name: Name):
        for user in self.data:
            if user.name == name:
                return user
        return None

    def commit(self, item: Buyer):
        for i, user in enumerate(self.data):
            if user == item:
                self.data[i] = item
                return "Success"
        return "failure"

    def delete(self, item: Buyer):
        for i, user in enumerate(self.data):
            if user == item:
                self.data.pop(i)
                return "Success"
        return "failure"
