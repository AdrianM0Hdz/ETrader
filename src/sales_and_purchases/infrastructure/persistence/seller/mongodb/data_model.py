"""
DATA MODEL FOR SELLER

MongoDB data model
{ 
    _id: <Object id> auto generated by mongodb
    id: <string uuid>
    name: <string>
    description: <string>
    products: [
        {   
            id: <string>
            name: <string>
            description: <string>
            price: {
                ammount: <float>
                currency: "MXN" | "USD"  
            }
            purchases: [
                {
                    "id": <"string uuid">
                    "buyerId": <string uuid>
                    "quantity": <int > 0>
                    "status": "TO_BE_DELIVERED" | "DELIVERED" | "CANCELLED"
                }...
            ]
        }...
    ]
}
"""
