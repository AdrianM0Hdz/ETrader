from flask import Flask, jsonify, request
from pymongo import MongoClient

from src.application.register_buyer import RegisterBuyer as RegisterBuyerService
from src.infrastructure.persistence.buyer.mongodb.repository import (
    MongoDBBuyerRepository,
)
from src.infrastructure.persistence.buyer.queries.buyer_query_set import BuyerQuerySet

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017")
buyer_collection = client.ETrader.buyer
buyer_repo = MongoDBBuyerRepository(buyer_collection=buyer_collection)
register_buyer_service = RegisterBuyerService(buyer_repo)
buyer_query_set = BuyerQuerySet(buyer_collection=buyer_collection)


@app.route("/resource/buyer", methods=["POST"])
def register_buyer():
    data = request.get_json()
    if not data:
        return jsonify(msg="no body found"), 400

    name = data["name"]
    register_buyer_service(name)

    return jsonify(msg="Ok")


@app.route("/queries/buyer/<string:id>", methods=["GET"])
def get_buyer(id):
    data = buyer_query_set.find_one_by_id(id)
    data["_id"] = str(data["_id"])
    return jsonify(**data)


if __name__ == "__main__":
    app.run(debug=True)
