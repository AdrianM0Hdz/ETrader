"""
Data model of something that happens here and there and there

MongoDB data model
{ 
    id: <string uuid>
    name: <string>
    products: [
        {   
            id: <string>
            name: <string>
            description: <string>
            price: {
                ammount: <float>
                currency: "MXN" | "USD" | ...  
            }
            purchases: [
                {
                    
                }...
            ]  
            
        }...
    ]
}
"""

from bson.objectid import ObjectId

from src.domain.seller import Seller, SellerData
