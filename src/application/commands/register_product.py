from src.domain.common.values import Name
from src.domain.common.values import Description

from src.domain.seller import Seller
from src.domain.seller.values import SellerId
from src.domain.seller.repository import SellerRepository

from src.domain.seller.entities.product.values import Price
from src.domain.seller.entities.product.enums import Cuerrency


class RegisterProduct:
    def __init__(self, seller_repository: SellerRepository):
        self.seller_repository = seller_repository

    def __call__(
        self,
        seller_id_str: str,
        product_name_str: str,
        product_description_str: str,
        price_ammount_float: float,
        price_currency_str: str,
    ):
        seller_id = SellerId(seller_id_str)
        seller = self.seller_repository.get(seller_id)

        product_name = Name(product_name_str)
        product_description = Description(product_description_str)
        currency = Cuerrency(price_currency_str)
        product_price = Price(price_ammount_float, currency)

        seller.register_product(product_name, product_description, product_price)

        self.seller_repository.commit(seller)
