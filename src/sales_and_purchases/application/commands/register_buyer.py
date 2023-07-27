from src.shared_kernel.application.observer.event_manager import EventManager
from src.shared_kernel.domain.events.buyer_created import BuyerCreated

from src.sales_and_purchases.domain.common.values import Name

from src.sales_and_purchases.domain.buyer import Buyer
from src.sales_and_purchases.domain.buyer.repository import BuyerRepository


class RegisterBuyer:
    def __init__(self, repo: BuyerRepository, event_manager: EventManager):
        self.repo = repo
        self.event_manager = event_manager

    def __call__(self, name: str):
        new_buyer = Buyer.create_new(Name(name))
        self.repo.add(new_buyer)
        self.event_manager.notify(
            BuyerCreated, BuyerCreated.create_new(new_buyer.id.value)
        )
