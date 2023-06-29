from dataclasses import dataclass
from uuid import uuid1


from domain.common.aggregate_root import Entity

from domain.buyer.values import BuyerId

from .values import PurchaseId, Quantity

from .enums import PurchaseStatus


class Purchase(Entity[PurchaseId]):
    def __init__(
        self, id: PurchaseId, buyer: BuyerId, quantity: Quantity, status: PurchaseStatus
    ):
        assert isinstance(id, PurchaseId)
        super().__init__(id)

        assert isinstance(buyer, BuyerId)
        assert isinstance(quantity, Quantity)

        self.__buyer = buyer
        self.__quantity = quantity
        self.__status = status

    @classmethod
    def create_new(cls, buyer: BuyerId, quantity: Quantity) -> "Purchase":
        id = PurchaseId(str(uuid1()))
        return cls(id, buyer, quantity, PurchaseStatus.TO_BE_DELIVERED)

    @property
    def buyer(self):
        return self.__buyer

    @property
    def quantity(self):
        return self.__quantity

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, new_status: PurchaseStatus):
        assert isinstance(new_status, PurchaseStatus)
        if (
            self.__status == PurchaseStatus.CANCELED
            or self.__status == PurchaseStatus.DELIVERED
        ):
            raise BaseException(
                "Cannot change the status of a cancelled or delivered order"
            )
        self.__status = new_status
