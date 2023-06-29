from src.domain.common.values import Name

from src.domain.buyer import Buyer
from src.domain.buyer.values import BuyerId
from src.domain.buyer.repository import BuyerRepository


class RegisterBuyer:
    def __init__(self, repo: BuyerRepository):
        self.repo = repo

    def __call__(self, name: str):
        new_buyer = Buyer.create_new(Name(name))
        self.repo.add(new_buyer)
