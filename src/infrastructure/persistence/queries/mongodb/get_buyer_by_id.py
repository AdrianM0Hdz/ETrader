from pymongo.collection import Collection

from src.application.queries.get_buyer_by_id import (
    GetBuyerById,
    BuyerPurchaseData,
    BuyerData,
)


class GetBuyerByIdMongoDB(GetBuyerById):
    def __init__(self, buyer_collection: Collection):
        self.buyer_collection = buyer_collection

    def _make_buyer_purchase_data(self, raw_data: dict) -> BuyerPurchaseData:
        return BuyerPurchaseData(
            id=raw_data["id"],
            seller_id=raw_data["sellerId"],
            product_id=raw_data["productId"],
            quantity=raw_data["quantity"],
            status=raw_data["status"],
        )

    def __call__(self, user_id: str) -> BuyerData:
        raw_data = self.buyer_collection.find_one({"id": user_id})

        if not raw_data:
            raise BaseException(f"user with {user_id} does not exist")

        return BuyerData(
            id=raw_data["id"],
            name=raw_data["name"],
            purchases=tuple(map(self._make_buyer_purchase_data, raw_data["purchases"])),
        )
