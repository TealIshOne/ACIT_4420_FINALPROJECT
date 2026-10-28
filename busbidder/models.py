
from dataclasses import dataclass
from datetime import datetime


##helper function
def yes_no(text):
    if text == "yes":
        return True
    if text== "no":
        return False
    raise ValueError(f"expected yes/no, got '{text}'")



## global variables and datasets
OFFER_TYPES={
    "offer_id": str,
    "company_id": str,
    "destination_id": str,
    "departure": datetime.fromisoformat,
    "arrival": datetime.fromisoformat,
    "duration_min": int,
    "price_eur": float,
    "transfers": int, 
    "luggage_kg": int,
    "changeable": yes_no,
    "refundable": yes_no,
    "seats_available": int,
    "stars": float,
    "co2_kg": float
}



@dataclass
class Company:
    company_id: str
    name: str
    profile: str

@dataclass
class Destination:
    destination_id: str
    name: str

@dataclass
class Offer:
    offer_id: str
    company_id: str
    destination_id: str
    departure: datetime
    arrival: datetime
    duration_min: int
    price_eur: float
    transfers: int
    luggage_kg: int
    changeable: bool
    refundable: bool
    seats_available: int
    stars: float
    co2_kg: float

    @classmethod                                  
    def from_row(cls, row):                      
        converted = {}
        for key, convert in OFFER_TYPES.items():
            converted[key] = convert(row[key])   
        return cls(**converted)

    

@dataclass
class Traveller:
    pass

@dataclass
class Booking:
    pass