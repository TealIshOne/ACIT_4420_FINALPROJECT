
from dataclasses import dataclass, field
from datetime import datetime
import re


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

WEIGHT_TYPES={
    "price": float,
    "flexibility": float,
    "departure_time": float,
    "duration": float,
    "co2": float
}

HARD_LIMITS_TYPES={
    "max_price_eur": float,
    "max_transfers": int,
    "min_luggage_kg": int,
    "changeable_required": bool,}

@dataclass
class Company:
    company_id: str
    name: str
    profile: str

@dataclass
class Destination:
    destination_id: str
    name: str

@dataclass (eq=False)
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
    profile_name: str
    hard_limits: dict
    weights: dict
    preferred_departure: str
    destination_id : str= None
    travel_date: str= None

    def weights_ok(self):
        for key in self.weights:
            if key not in WEIGHT_TYPES:
                raise ValueError(f"invalid weight: {key}")
        return sum(self.weights.values()) == 100

    def hard_limits_ok(self):
        for key in self.hard_limits:
            if key not in HARD_LIMITS_TYPES:
                raise ValueError(f"invalid hard limit: {key}")
        return True

    def departure_time_ok(self):
        try:
            datetime.strptime(self.preferred_departure, "%H:%M")
            return True
        except ValueError:
            raise ValueError(f"invalid departure time: {self.preferred_departure}")
    @classmethod
    def from_profile(cls, profile_name, profiles):
        profile=profiles[profile_name]
        return cls(
            profile_name=profile_name,
            hard_limits=profile["hard_limits"],
            weights=profile["weights"],
            preferred_departure=profile["preferred_departure"]
        )



@dataclass
class Booking:
    chosen_offer: Offer
    booking_ref: str 
    booking_time: datetime = field(default_factory=datetime.now)


