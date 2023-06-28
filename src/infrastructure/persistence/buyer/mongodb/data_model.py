"""
Creates mongodb representation of user entity

MongoDB Data Model: 
{
    "id": <string uuid>
    "name": <string>
    "purchases": [
        <purchase object>
    ] managed by seller repository but placed here for query performance
}

"""

from bson.objectid import ObjectId
from src.domain.buyer import Buyer
from src.domain.buyer.buyer import BuyerData


def make_data_model_from_domain_model(buyer: BuyerData):
    return {"id": buyer.id.value, "name": buyer.name.value, "purchases": []}


def make_domain_model_from_data_model(buyer: dict) -> Buyer:
    return Buyer(buyer["id"], buyer["name"])
