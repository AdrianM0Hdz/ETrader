from src.shared_kernel.application.observer.event_manager import EventManager
from src.shared_kernel.domain.events.seller_created import SellerCreated

from src.sales_and_purchases.domain.common.values import Name
from src.sales_and_purchases.domain.common.values import Description

from src.sales_and_purchases.domain.seller import Seller
from src.sales_and_purchases.domain.seller.repository import SellerRepository


class RegisterSeller:
    def __init__(
        self, seller_repository: SellerRepository, event_manager: EventManager
    ):
        self.seller_repository = seller_repository
        self.event_manager = event_manager

    def __call__(self, name: str, description: str):
        seller = Seller.create_new(
            name=Name(name), description=Description(description)
        )
        self.seller_repository.add(seller)
        self.event_manager.notify(
            SellerCreated, SellerCreated.create_new(seller_id=seller.id.value)
        )
