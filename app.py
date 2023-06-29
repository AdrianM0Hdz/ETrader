from flask import Flask, jsonify, request
from pymongo import MongoClient

from src.application.register_buyer import RegisterBuyer as RegisterBuyerService
from src.infrastructure.persistence.buyer.mongodb.repository import (
    MongoDBBuyerRepository,
)

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

from src.infrastructure.persistence.seller.mongodb.repository import (
    MongoDBSellerRepository,
)

from src.infrastructure.persistence.buyer.queries.buyer_query_set import BuyerQuerySet

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017")

buyer_collection = client.ETrader.buyer
seller_collection = client.ETrader.seller

buyer_repo = MongoDBBuyerRepository(buyer_collection=buyer_collection)
seller_repo = MongoDBSellerRepository(
    seller_collection=seller_collection, buyer_collection=buyer_collection
)

register_buyer_service = RegisterBuyerService(buyer_repo)
buyer_query_set = BuyerQuerySet(buyer_collection=buyer_collection)

register_seller_service = RegisterSellerService(seller_repo)
register_product_servie = RegisterProductService(seller_repo)
register_purchase_service = RegisterPurchaseService(seller_repo)
mark_purchase_as_delivered_service = MarkPurchaseAsDeliveredService(seller_repo)
mark_purchase_as_canceled_service = MarkPurchaseAsCanceledService(seller_repo)

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


@app.route("/queries/buyer/<string:id>", methods=["GET"])
def get_buyer(id):
    data = buyer_query_set.find_one_by_id(id)
    if data is None:
        return jsonify(), 400
    data["_id"] = str(data["_id"])
    return jsonify(**data)


if __name__ == "__main__":
    app.run(debug=True)
