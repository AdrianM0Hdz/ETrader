from src.domain.seller.values import SellerId
from src.domain.seller.repository import SellerRepository

from src.domain.seller.entities.product.values import ProductId

from src.domain.seller.entities.purchase.values import PurchaseId


class MarkPurchaseAsDelivered:
    def __init__(self, seller_repository: SellerRepository):
        self.seller_repository = seller_repository

    def __call__(
        self,
        seller_id_str: str,
        product_id_str: str,
        purchase_id_str: str,
    ):
        seller_id = SellerId(seller_id_str)
        product_id = ProductId(product_id_str)
        purchase_id = PurchaseId(purchase_id_str)

        seller = self.seller_repository.get(seller_id)
        seller.mark_purchase_delivered(product_id, purchase_id)
        self.seller_repository.commit(seller)
