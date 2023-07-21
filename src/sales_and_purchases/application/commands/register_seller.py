from src.sales_and_purchases.domain.common.values import Name
from src.sales_and_purchases.domain.common.values import Description

from src.sales_and_purchases.domain.seller import Seller
from src.sales_and_purchases.domain.seller.repository import SellerRepository


class RegisterSeller:
    def __init__(self, seller_repository: SellerRepository):
        self.seller_repository = seller_repository

    def __call__(self, name: str, description: str):
        seller = Seller.create_new(
            name=Name(name), description=Description(description)
        )
        self.seller_repository.add(seller)
