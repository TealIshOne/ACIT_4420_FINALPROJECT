#home brew
from busbidder.models import Offer
from busbidder.errors import BusBidderError,InvalidOfferError, InvalidIdentifierError

# libs
import re
from datetime import datetime
import logging

rejects_logger =logging.getLogger("rejects")


OFFER_ID_CODE=re.compile(r"^OF-\d{4}$")

ALL_OFFER_ITEMS=[
    "offer_id", 
    "company_id", 
    "destination_id", 
    "departure", 
    "arrival", 
    "duration_min", 
    "price_eur", 
    "transfers", 
    "luggage_kg", 
    "changeable", 
    "refundable", 
    "seats_available",
    "stars",
    "co2_kg"
    ]
ALL_DESTINATION_IDS=[
    "BAR",
    "VAL",
    "SEV",
    "MAL",
    "GRA",
    "COR",
    "BIL",
    "SSB",
    "ZAR",
    "ALI",
    "MUR",
    "SAL",
    "TOL",
    "SCQ",
    "CAD"
    ]

ALL_COMPANY_IDS=[
    "solruta",
    "camino",
    "costalink",
    "verdebus",
    "nochevia"
    ]
def check_types(row):
    '''
    checks if type convertion is sucsessful
    '''
    try:
        return Offer.from_row(row)
    except ValueError as err:
        raise InvalidOfferError(row["offer_id"], f"bad type: {err}") from err


def check_columns(row):
    '''
    checks if all items are present
    '''

    for name in ALL_OFFER_ITEMS:
        if name not in row or row[name] in ("", None):
            raise InvalidOfferError(row.get("offer_id"), f"missing value:{name}")


def check_id_format(row):
    '''
    checks if the id is correct regex
    '''
    offer_id=row["offer_id"]
    if not OFFER_ID_CODE.fullmatch(offer_id):
        raise InvalidIdentifierError(offer_id, "offer_id", OFFER_ID_CODE.pattern)


def check_unique_id(row, seen_ids):
    '''
    ensures an offer id is only used once
    '''
    offer_id=row["offer_id"]
    if offer_id in seen_ids:
        raise InvalidIdentifierError (offer_id, "duplicate offer_id")
    seen_ids.add(offer_id)


def check_destination(row):
    '''
    ensures destination is defined in destinations.csv
    '''
    dest_id=row["destination_id"]
    if dest_id not in ALL_DESTINATION_IDS:
        raise InvalidOfferError(row["offer_id"], f"unknown destination: {dest_id}")


def check_company(row):
    '''
    ensures company is defined in companies.csv
    '''
    comp_id=row["company_id"]
    if comp_id not in ALL_COMPANY_IDS:
        raise InvalidOfferError(row["offer_id"], f"unknown company: {comp_id}")


def check_price(offer):
    '''
    tags and rejects negatice prices 
    '''
    price= offer.price_eur
    if price<0:
        raise InvalidOfferError(offer.offer_id, f"negative price: {price}")


def check_timetravel(offer):
    '''
    checks departure before arrival
    '''
    departure =offer.departure
    arrival = offer.arrival

    if arrival < departure :
        raise InvalidOfferError(offer.offer_id, f"TIMETRAVEL: arrival before departure")


def check_stars(offer):
    '''
    checks if stars/rating is within bounds 1-5
    '''
    stars=offer.stars
    if stars < 1 or stars > 5:
        raise InvalidOfferError(offer.offer_id, f"stars outside 1-5: {stars}")


def check_seats(offer):
    '''
    checks for negative seats,
    '''
    remaining_seats=offer.seats_available
    if remaining_seats<1:
        raise InvalidOfferError(offer.offer_id, f"negative seats: {remaining_seats}")


def check_transfers(offer):
    '''
    checks for negatice transfers
    '''
    nr_trans=offer.transfers
    if nr_trans<0:
        raise InvalidOfferError(offer.offer_id, f"negative transfers: {nr_trans}")


def check_duration(offer):
    '''
    checks if duration matches arrival-departure
    '''
    departure =offer.departure
    arrival = offer.arrival
    duration=offer.duration_min
    dur_check=(arrival-departure).total_seconds()/60
    if duration!=dur_check:
        raise InvalidOfferError(offer.offer_id, f"duration {duration} does not match travel time {dur_check}")


def check_co2(offer):
    '''
    checks for negative co2
    '''
    co2=offer.co2_kg
    if co2<0:
        raise InvalidOfferError(offer.offer_id, f"negative co2: {co2}")

def check_luggage(offer):
    '''
    checks for negative luggage
    '''
    luggage=offer.luggage_kg
    if luggage<0:
        raise InvalidOfferError(offer.offer_id, f"negative luggage: {luggage}")



### ---------------summerising function --------------------###

def validate_offers(rows):
    '''
    calls all previous functions, start with id format
    stores two data sets, valid and rejected rows
    '''
    valid=[]
    rejected=[]
    seen_ids=set()
    for row in rows:
        try:
            check_columns(row)
            check_id_format(row)
            check_destination(row)
            check_company(row)
            offer= check_types(row)
            check_price(offer)
            check_timetravel(offer)
            check_stars(offer)
            check_seats(offer)
            check_transfers(offer)
            check_duration(offer)
            check_co2(offer)
            check_luggage(offer)
            check_unique_id(row,seen_ids)

            valid.append(offer)
        except BusBidderError as err:
            rejected.append((row,str(err)))
            rejects_logger.warning("rejection: %s", err)

    return valid, rejected


