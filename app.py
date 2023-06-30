from flask import Flask, jsonify, request
from pymongo import MongoClient

from src.application.register_buyer import RegisterBuyer as RegisterBuyerService
from src.infrastructure.persistence.buyer.mongodb.repository import (
    MongoDBBuyerRepository,
)

# COMMANDS

from src.application.commands.register_seller import (
    RegisterSeller as RegisterSellerService,
)
from src.application.commands.register_product import (
    RegisterProduct as RegisterProductService,
)
from src.application.commands.register_purchase import (
    RegisterPurchase as RegisterPurchaseService,
)
from src.application.commands.mark_purchase_as_delivered import (
    MarkPurchaseAsDelivered as MarkPurchaseAsDeliveredService,
)
from src.application.commands.mark_purchase_as_canceled import (
    MarkPurchaseAsCanceled as MarkPurchaseAsCanceledService,
)

# QUERIES

from src.application.queries.get_buyer_by_id import (
    GetBuyerById as GetBuyerByIdService,
    BuyerPurchaseData,
)


from src.infrastructure.persistence.seller.mongodb.repository import (
    MongoDBSellerRepository,
)

from src.infrastructure.persistence.queries.mongodb.get_buyer_by_id import (
    GetBuyerByIdMongoDB,
)


app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017")

buyer_collection = client.ETrader.buyer
seller_collection = client.ETrader.seller

buyer_repo = MongoDBBuyerRepository(buyer_collection=buyer_collection)
seller_repo = MongoDBSellerRepository(
    seller_collection=seller_collection, buyer_collection=buyer_collection
)

# command use cases

register_buyer_service = RegisterBuyerService(buyer_repo)

register_seller_service = RegisterSellerService(seller_repo)
register_product_servie = RegisterProductService(seller_repo)
register_purchase_service = RegisterPurchaseService(seller_repo)
mark_purchase_as_delivered_service = MarkPurchaseAsDeliveredService(seller_repo)
mark_purchase_as_canceled_service = MarkPurchaseAsCanceledService(seller_repo)

# queries use cases

# just assigned to a variable to avoid thight coupling
get_buyer_by_id_service: GetBuyerByIdService = GetBuyerByIdMongoDB(
    buyer_collection=buyer_collection
)

### COMMANDS ###


@app.route("/resource/buyer", methods=["POST"])
def register_buyer():
    data = request.get_json()
    if not data:
        return jsonify(msg="no body found"), 400

    name = data["name"]
    register_buyer_service(name)

    return jsonify(msg="Ok")


@app.route("/resource/seller", methods=["POST"])
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
        seller_id_str=data["seller_id"],
        product_name_str=data["product_name"],
        product_description_str=data["product_description"],
        price_ammount_float=data["price_ammount"],
        price_currency_str=data["price_currency"],
    )

    return jsonify(msg="OK")


@app.route("/command/register_purchase", methods=["POST"])
def register_purchase():
    data = request.get_json()
    if not data:
        return jsonify(msg="no body found"), 400

    register_purchase_service(
        buyer_id_str=data["buyer_id"],
        seller_id_str=data["seller_id"],
        product_id_str=data["product_id"],
        quantity_int=data["quantity"],
    )

    return jsonify(msg="OK")


@app.route("/command/mark_purchase_as_delivered", methods=["POST"])
def mark_purchase_as_delivered():
    data = request.get_json()
    if not data:
        return jsonify(msg="no body found"), 400

    mark_purchase_as_delivered_service(
        seller_id_str=data["seller_id"],
        product_id_str=data["product_id"],
        purchase_id_str=data["purchase_id"],
    )
    return jsonify(msg="OK")


@app.route("/command/mark_purchase_as_canceled", methods=["POST"])
def mark_purchase_as_canceled():
    data = request.get_json()
    if not data:
        return jsonify(msg="no body found"), 400

    mark_purchase_as_canceled_service(
        seller_id_str=data["seller_id"],
        product_id_str=data["product_id"],
        purchase_id_str=data["purchase_id"],
    )
    return jsonify(msg="OK")


### QUERIES ###


@app.route("/query/get_buyer_by_id", methods=["GET"])
def get_buyer_by_id():
    def _buyer_purchase_data_to_dict(data: BuyerPurchaseData):
        return {
            "id": data.id,
            "sellerId": data.seller_id,
            "productId": data.product_id,
            "quantity": data.quantity,
            "status": data.status,
        }

    data = request.get_json()
    if not data:
        return jsonify(msg="no body found"), 400

    raw_buyer_id = data["userId"]
    buyer_data = get_buyer_by_id_service(user_id=raw_buyer_id)

    return jsonify(
        id=buyer_data.id,
        name=buyer_data.name,
        purchases=list(map(_buyer_purchase_data_to_dict, buyer_data.purchases)),
    )


if __name__ == "__main__":
    app.run(debug=True)
