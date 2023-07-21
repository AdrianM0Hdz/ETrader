from src.sales_and_purchases.domain.buyer.values import BuyerId

from src.sales_and_purchases.domain.seller import Seller
from src.sales_and_purchases.domain.seller.values import SellerId
from src.sales_and_purchases.domain.seller.repository import SellerRepository

from src.sales_and_purchases.domain.seller.entities.product.values import ProductId
from src.sales_and_purchases.domain.seller.entities.purchase.values import Quantity


class RegisterPurchase:
    def __init__(self, seller_repository: SellerRepository):
        self.seller_repository = seller_repository

    def __call__(
        self,
        buyer_id_str: str,
        seller_id_str: str,
        product_id_str: str,
        quantity_int: int,
    ):
        buyer_id = BuyerId(buyer_id_str)
        seller_id = SellerId(seller_id_str)
        quantity = Quantity(quantity_int)
        product_id = ProductId(product_id_str)

        seller = self.seller_repository.get(seller_id)
        seller.register_purchase(product_id, buyer_id, quantity)
        self.seller_repository.commit(seller)
