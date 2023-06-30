from typing import Tuple, List

from pymongo.collection import Collection

from src.application.queries.get_seller_by_id import (
    GetSellerById,
    SellerData,
    SellerProductData,
    ProductPriceData,
    ProductPurchaseData,
)


class GetSellerByIdMongoDB(GetSellerById):
    def __init__(self, seller_collection: Collection):
        self.seller_collection = seller_collection

    def _make_product_purchase_data(self, raw_purchase: dict) -> ProductPurchaseData:
        return ProductPurchaseData(
            id=raw_purchase["id"],
            buyer_id=raw_purchase["buyerId"],
            quantity=raw_purchase["quantity"],
            status=raw_purchase["status"],
        )

    def _make_product_purchase_data_tuple(
        self, raw_purchase_list: List[dict]
    ) -> Tuple[ProductPurchaseData]:
        return tuple(map(self._make_product_purchase_data, raw_purchase_list))

    def _make_product_price_data(self, raw_price) -> ProductPriceData:
        return ProductPriceData(
            ammount=raw_price["ammount"], currency=raw_price["currency"]
        )

    def _make_seller_product_data(self, raw_product: dict) -> SellerProductData:
        return SellerProductData(
            id=raw_product["id"],
            name=raw_product["name"],
            description=raw_product["description"],
            price=self._make_product_price_data(raw_product["price"]),
            purchases=self._make_product_purchase_data_tuple(raw_product["purchases"]),
        )

    def _make_seller_product_data_tuple(
        self, raw_product_list: List[dict]
    ) -> Tuple[SellerProductData]:
        return tuple(map(self._make_seller_product_data, raw_product_list))

    def __call__(self, seller_id: str) -> SellerData:
        raw_data = self.seller_collection.find_one({"id": seller_id})
        if not raw_data:
            raise BaseException(f"no seller with id {seller_id} found")

        return SellerData(
            id=raw_data["id"],
            name=raw_data["name"],
            description=raw_data["description"],
            products=self._make_seller_product_data_tuple(raw_data["products"]),
        )
