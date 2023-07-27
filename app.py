from typing import List, Tuple

from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient

from src.sales_and_purchases.application.commands.register_buyer import (
    RegisterBuyer as RegisterBuyerService,
)
from src.sales_and_purchases.infrastructure.persistence.buyer.mongodb.repository import (
    MongoDBBuyerRepository,
)

# COMMANDS

from src.sales_and_purchases.application.commands.register_seller import (
    RegisterSeller as RegisterSellerService,
)
from src.sales_and_purchases.application.commands.register_product import (
    RegisterProduct as RegisterProductService,
)
from src.sales_and_purchases.application.commands.register_purchase import (
    RegisterPurchase as RegisterPurchaseService,
)
from src.sales_and_purchases.application.commands.mark_purchase_as_delivered import (
    MarkPurchaseAsDelivered as MarkPurchaseAsDeliveredService,
)
from src.sales_and_purchases.application.commands.mark_purchase_as_canceled import (
    MarkPurchaseAsCanceled as MarkPurchaseAsCanceledService,
)

# QUERIES

from src.sales_and_purchases.application.queries.get_buyer_by_id import (
    GetBuyerById as GetBuyerByIdService,
    BuyerPurchaseData,
)


from src.sales_and_purchases.application.queries.get_seller_by_id import (
    GetSellerById as GetSellerByIdService,
    SellerData,
    SellerProductData,
    ProductPriceData,
    ProductPurchaseData,
)

from src.sales_and_purchases.infrastructure.persistence.seller.mongodb.repository import (
    MongoDBSellerRepository,
)

from src.sales_and_purchases.infrastructure.persistence.queries.mongodb.get_buyer_by_id import (
    GetBuyerByIdMongoDB,
)
from src.sales_and_purchases.infrastructure.persistence.queries.mongodb.get_seller_by_id import (
    GetSellerByIdMongoDB,
)

from src.shared_kernel.infrastructure.observer.event_manager import (
    ConcreteEventManager,
)

from src.auth.application.commands.register_user_credentials import (
    RegisterUserCredentials,
)
from src.auth.application.commands.verify_user_password import VerifyUserPassword

from src.auth.infrastructure.persistence.user_credentials.mongodb.repository import (
    MongoDBUserCredentialsRepository,
)
from src.auth.infrastructure.observer.subscriber import UserCreationSubscriber

from src.shared_kernel.domain.events.seller_created import SellerCreated
from src.shared_kernel.domain.events.buyer_created import BuyerCreated


# observer infrastructure
event_manager = ConcreteEventManager()

app = Flask(__name__)
CORS(app)
client = MongoClient("mongodb://localhost:27017")

buyer_collection = client.ETrader.buyer
seller_collection = client.ETrader.seller
credentials_collection = client.ETrader.user_credentials

buyer_repo = MongoDBBuyerRepository(buyer_collection=buyer_collection)
seller_repo = MongoDBSellerRepository(
    seller_collection=seller_collection, buyer_collection=buyer_collection
)
user_credentials_repo = MongoDBUserCredentialsRepository(
    user_credentials_collection=credentials_collection
)

# command use cases

register_buyer_service = RegisterBuyerService(buyer_repo, event_manager)

register_seller_service = RegisterSellerService(seller_repo, event_manager)
register_product_servie = RegisterProductService(seller_repo)
register_purchase_service = RegisterPurchaseService(seller_repo)
mark_purchase_as_delivered_service = MarkPurchaseAsDeliveredService(seller_repo)
mark_purchase_as_canceled_service = MarkPurchaseAsCanceledService(seller_repo)

# queries use cases

# just assigned to a variable to avoid thight coupling
get_buyer_by_id_service: GetBuyerByIdService = GetBuyerByIdMongoDB(
    buyer_collection=buyer_collection
)
get_seller_by_id_service: GetSellerByIdService = GetSellerByIdMongoDB(
    seller_collection=seller_collection
)


# user cretentials use cases

register_user_credentials = RegisterUserCredentials(
    user_credentials_repository=user_credentials_repo
)

verify_user_password = VerifyUserPassword(
    user_credentials_repository=user_credentials_repo
)

user_creation_subscriber = UserCreationSubscriber(
    register_user_credentials_service=register_user_credentials
)
event_manager.subscribe(SellerCreated, user_creation_subscriber)
event_manager.subscribe(BuyerCreated, user_creation_subscriber)


### COMMANDS ###


@app.route("/command/register_buyer", methods=["POST"])
def register_buyer():
    data = request.get_json()
    if not data:
        return jsonify(msg="no body found"), 400

    name = data["name"]
    register_buyer_service(name)

    return jsonify(msg="OK")


@app.route("/command/register_seller", methods=["POST"])
def register_seller():
    data = request.get_json()
    if not data:
        return jsonify(msg="no body found"), 400

    name = data["name"]
    description = data["description"]

    register_seller_service(name, description)

    return jsonify(msg="OK")


@app.route("/command/register_product", methods=["POST"])
def register_product():
    data = request.get_json()
    if not data:
        return jsonify(msg="no body found"), 400

    register_product_servie(
        seller_id_str=data["sellerId"],
        product_name_str=data["name"],
        product_description_str=data["description"],
        price_ammount_float=data["price"]["ammount"],
        price_currency_str=data["price"]["currency"],
    )

    return jsonify(msg="OK")


@app.route("/command/register_purchase", methods=["POST"])
def register_purchase():
    data = request.get_json()
    if not data:
        return jsonify(msg="no body found"), 400

    register_purchase_service(
        buyer_id_str=data["buyerId"],
        seller_id_str=data["sellerId"],
        product_id_str=data["productId"],
        quantity_int=data["quantity"],
    )

    return jsonify(msg="OK")


@app.route("/command/mark_purchase_as_delivered", methods=["POST"])
def mark_purchase_as_delivered():
    data = request.get_json()
    if not data:
        return jsonify(msg="no body found"), 400

    mark_purchase_as_delivered_service(
        seller_id_str=data["sellerId"],
        product_id_str=data["productId"],
        purchase_id_str=data["purchaseId"],
    )
    return jsonify(msg="OK")


@app.route("/command/mark_purchase_as_canceled", methods=["POST"])
def mark_purchase_as_canceled():
    data = request.get_json()
    if not data:
        return jsonify(msg="no body found"), 400

    mark_purchase_as_canceled_service(
        seller_id_str=data["sellerId"],
        product_id_str=data["productId"],
        purchase_id_str=data["purchaseId"],
    )
    return jsonify(msg="OK")


### QUERIES ###


@app.route("/query/get_buyer_by_id", methods=["POST"])
def get_buyer_by_id():
    def _buyer_purchase_data_to_dict(data: BuyerPurchaseData) -> dict:
        return {
            "id": data.id,
            "sellerId": data.seller_id,
            "productId": data.product_id,
            "quantity": data.quantity,
            "status": data.status,
        }

    data = request.get_json()

    if not data or data == {}:
        return jsonify(msg="no body found"), 400

    raw_buyer_id = data["id"]
    buyer_data = get_buyer_by_id_service(user_id=raw_buyer_id)

    return jsonify(
        id=buyer_data.id,
        name=buyer_data.name,
        purchases=list(map(_buyer_purchase_data_to_dict, buyer_data.purchases)),
    )


@app.route("/query/get_seller_by_id", methods=["POST"])
def get_seller_by_id():
    def _product_purchase_data_to_dict(data: ProductPurchaseData) -> dict:
        return {
            "id": data.id,
            "buyerId": data.buyer_id,
            "quantity": data.quantity,
            "status": data.status,
        }

    def _product_purchase_data_tuple_to_list(
        data: Tuple[ProductPurchaseData],
    ) -> List[dict]:
        return list(map(_product_purchase_data_to_dict, data))

    def _product_price_data_to_dict(data: ProductPriceData) -> dict:
        return {"ammount": data.ammount, "currency": data.currency}

    def _seller_product_data_to_dict(data: SellerProductData) -> dict:
        return {
            "id": data.id,
            "name": data.name,
            "description": data.description,
            "price": _product_price_data_to_dict(data.price),
            "purchases": _product_purchase_data_tuple_to_list(data.purchases),
        }

    def _seller_product_data_tuple_to_list(
        data: Tuple[SellerProductData],
    ) -> List[dict]:
        return list(map(_seller_product_data_to_dict, data))

    data = request.get_json()
    if not data:
        return jsonify(msg="no body found"), 400

    raw_seller_id = data["id"]
    seller_data = get_seller_by_id_service(seller_id=raw_seller_id)

    return jsonify(
        id=seller_data.id,
        name=seller_data.name,
        description=seller_data.description,
        products=_seller_product_data_tuple_to_list(seller_data.products),
    )


if __name__ == "__main__":
    app.run(debug=True)
