from src.shared_kernel.application.observer.subscriber import Subscriber
from src.shared_kernel.domain.events.event import Event
from src.shared_kernel.domain.events.buyer_created import BuyerCreated
from src.shared_kernel.domain.events.seller_created import SellerCreated

from src.auth.application.commands.register_user_credentials import (
    RegisterUserCredentials,
)


class UserCreationSubscriber(Subscriber):
    def __init__(self, register_user_credentials_service: RegisterUserCredentials):
        self.register_user_credentials_service = register_user_credentials_service

    def update(self, event: Event):
        if isinstance(event, BuyerCreated):
            self.register_user_credentials_service(event.buyer_id)
        elif isinstance(event, SellerCreated):
            self.register_user_credentials_service(event.seller_id)
