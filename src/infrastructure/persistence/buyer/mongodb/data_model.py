"""

MongoDB Data Model: 
{
    "_id": <ObjectId> auto generated by mongodb
    "id": <string uuid>
    "name": <string>
    "purchases": [
        {
            "productId": <string>
            "quantity": <int > 0>
            "status": "TO_BE_DELIVERED" | "DELIVERED" | "CANCELED"
        } ...
    ], managed by seller repository but placed here for query performance via denormalization
}
"""
