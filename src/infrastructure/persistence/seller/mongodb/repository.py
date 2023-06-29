from typing import List, Dict

from pymongo.collection import Collection

from src.domain.common.values import Name, Description

from src.domain.buyer.values import BuyerId

from src.domain.seller import Seller
from src.domain.seller.values import SellerId
from src.domain.seller.repository import SellerRepository

from src.domain.seller.entities.product.product import Product
from src.domain.seller.entities.product.values import ProductId, Price
from src.domain.seller.entities.product.enums import Cuerrency

from src.domain.seller.entities.purchase.purchase import Purchase
from src.domain.seller.entities.purchase.values import PurchaseId, Quantity
from src.domain.seller.entities.purchase.enums import PurchaseStatus


class MongoDBSellerRepository(SellerRepository):
    def __init__(self, seller_collection: Collection, buyer_collection: Collection):
        self.seller_collection = seller_collection
        self.buyer_collection = buyer_collection

    def _seller_already_exists(self, item: Seller):
        data = self.seller_collection.find_one({"id": item.id.value})
        return data is not None

    def _serialyze_purchase(self, purchase: Purchase) -> dict:
        """Creates data model representation of a purchase"""
        return {
            "id": purchase.id.value,
            "buyerId": purchase.buyer.value,
            "quantity": purchase.quantity.value,
            "status": purchase.status.value,
        }

    def _deserialize_purchase(self, purchase_data: dict) -> Purchase:
        """Returns Purchase domain object from data dict"""
        return Purchase(
            id=PurchaseId(purchase_data["id"]),
            buyer=BuyerId(purchase_data["buyerId"]),
            quantity=Quantity(purchase_data["quantity"]),
            status=PurchaseStatus(purchase_data["status"]),
        )

    def _serialyze_product(self, product: Product, purchases: List[Purchase]) -> dict:
        """Creates data model representation of a product"""
        return {
            "id": product.id.value,
            "name": product.name.value,
            "description": product.description.value,
            "price": {
                "ammount": product.price.ammount,
                "currency": product.price.currency.value,
            },
            "purchases": list(map(self._serialyze_purchase, purchases)),
        }

    def _deserialize_product(self, product_data: dict) -> Product:
        """Returns Product domain object from data dict"""
        return Product(
            id=ProductId(product_data["id"]),
            name=Name(product_data["name"]),
            description=Description(product_data["description"]),
            price=Price(
                ammount=product_data["price"]["ammount"],
                currency=Cuerrency(product_data["price"]["currency"]),
            ),
        )

    def _serialize_seller(self, seller: Seller) -> dict:
        return {
            "id": seller.id.value,
            "name": seller.name.value,
            "description": seller.description.value,
            "products": list(
                map(
                    lambda product: self._serialyze_product(
                        product, seller.get_purchases_of_product(product)
                    ),
                    seller.products,
                )
            ),
        }

    def _make_product_to_purchases_dict(
        self, products_data: List[dict]
    ) -> Dict[Product, List[Purchase]]:
        """Takes a list of product data and converts it to dict and purchase pair"""
        d = {}
        for product_data in products_data:
            product = self._deserialize_product(product_data)
            purchases = list(map(self._deserialize_purchase, product_data["purchases"]))
            d[product] = purchases
        return d

    def _deserialize_seller(self, seller_data: dict) -> Seller:
        return Seller(
            id=SellerId(seller_data["id"]),
            name=Name(seller_data["name"]),
            description=Description(seller_data["description"]),
            products=self._make_product_to_purchases_dict(seller_data["products"]),
        )

    def add(self, item: Seller):
        if self._seller_already_exists(item):
            raise ValueError("seller with such id already exists")
        self.seller_collection.insert_one(self._serialize_seller(item))

    def get(self, id: SellerId) -> Seller:
        data = self.seller_collection.find_one({"id": id.value})
        if data is None:
            raise FileNotFoundError("seller not found")
        return self._deserialize_seller(data)

    def commit(self, item: Seller):
        if not self._seller_already_exists(item):
            raise ValueError("cannot commit an item that does not exist")
        self.seller_collection.update_one(
            {"id": item.id.value},
            {"$set": self._serialize_seller(item)},
        )
        for product in item.products:
            for purchases in item.get_purchases_of_product(product):
                for purchase in purchases:
                    buyer_data = self.buyer_collection.find_one(
                        {"id": purchase.buyer.value}
                    )

    def delete(self, item: Seller):
        if not self._seller_already_exists(item):
            raise ValueError("cannot delete item that does not exist")
