from flask import Flask, jsonify, request

from ..application.register_buyer import RegisterBuyer as RegisterBuyerService
from .persistence.buyer.mock.repository import MockBuyerRepository

app = Flask(__name__)
buyer_repo = MockBuyerRepository()
register_buyer_service = RegisterBuyerService(buyer_repo)


@app.route("/resource/buyer", methods=["POST"])
def register_buyer():
    data = request.get_json()
    if not data:
        return jsonify(msg="no body found"), 400

    name = data["name"]
    assert isinstance(name, str)

    register_buyer_service(name)

    return jsonify(msg="Ok")


if __name__ == "__name__":
    app.run(debug=True)
