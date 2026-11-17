import re
import uuid
import json
from pathlib import Path
from datetime import datetime
import logging
from busbidder.models import Traveller, Booking
from busbidder.loader import call_files
from busbidder.validation import validate_offers
from busbidder.filters import passes_hard_limits, weights_score
from busbidder.ranking import rank_offers
from busbidder.errors import BookingError
from busbidder.explain import explain_top_offer



BOOKING_REFERENCE_CODE = re.compile(r"^BK-[0-9A-F]{8}$")
                                    # CHANGED: new import at top

OUT_DIR = Path(__file__).resolve().parent.parent / "outputs"  

booking_logger=logging.getLogger("bookings")


## helper functions:
def make_booking_ref():
    ref="BK-" + uuid.uuid4().hex[:8].upper()
    return ref


def booked_seats():
    file = OUT_DIR /"bookings.json"
    counts={}
    if file.exists():
        with open(file, encoding="utf-8") as f:
            for b in json.load(f):
                counts[b["offer_id"]]= counts.get(b["offer_id"],0)+1
    return counts

def show_profiles(profiles=None):
    if profiles is None:
        profiles = {}
    names=list(profiles)
    for number, name in enumerate(names, start=1):
        print(f"{number}. {profiles[name]['label']}")
        print(f"  hard limits: {profiles[name]['hard_limits']}")
        print(f"  weights:     {profiles[name]['weights']}")

def ask_profile(profiles=None):
    if profiles is None:
        profiles = {}
    names=list(profiles)
    for number, name in enumerate(names, start=1):
        print(f"{number}. {profiles[name]['label']}")
    while True:
        choice =input("Choose a profile by number: ")
        if choice == "+":
            show_profiles(profiles)
            continue
        if choice.isdigit() and 1 <= int(choice) <= len(names):
            return names[int(choice)-1]
        print("Invalid choice. Please enter a number corresponding to the profile.")






def ask_destination(destinations=None):
    if destinations is None:
        destinations = []

    for number, dest in enumerate(destinations, start=1):
        print(f"{number}. {dest['destination_id']}: {dest['destination']}")
    while True:
        choice = input("Choose a destination by number: ")
        if choice.isdigit() and 1 <= int(choice) <= len(destinations):
            return destinations[int(choice)-1]["destination_id"]
        print("Invalid choice. Please enter a number corresponding to the destination.")


def ask_travel_date(date_time=None):
    while True:
        date_input=input(f"enter perferede travel date: ")
        if date_input == "":
            return date_time
        try:
            datetime.strptime(date_input, "%B %d %Y")
            return date_input
        except ValueError:
            print("invalid date format, please enter in month dd, yyyy format.")


def ask_departure_time(departure_time=None):
    while True:
        time_input = input(f"Enter preferred departure time (HH:MM) : ")
        if time_input == "":
            return departure_time
        try:
            datetime.strptime(time_input, "%H:%M")
            return time_input
        except ValueError:
            print("Invalid time format. Please enter in HH:MM format.")


def Travlers_choices():
    # traveler must be able to choose destination, data, a profile. changes to profile 
    profiles = call_files(["prof"])["prof"]
    destinations = call_files(["dest"])["dest"]
    prof= ask_profile(profiles)
    traveller=Traveller.from_profile(prof, profiles)
    traveller.destination_id= ask_destination(destinations)
    traveller.travel_date=ask_travel_date()
    traveller.preferred_departure =ask_departure_time(traveller.preferred_departure)

    return traveller




def booking_choices(travler):
    files=  call_files(["bad", "off"])
    offers= files['off'] + files['bad']


    valid_off, reject_off = validate_offers(offers)

    booked= booked_seats()
    for o in valid_off:
        o.seats_available = o.seats_available - booked.get(o.offer_id,0)
    valid_off = [o for o in valid_off if o.seats_available > 0]
    valid_off = [o for o in valid_off if o.destination_id == travler.destination_id] 
    if travler.travel_date:
        wanted_date=datetime.strptime(travler.travel_date, "%B %d %Y").date()
        valid_off= [o for o in valid_off if o.departure.date() == wanted_date]
    pass_hl_offers=passes_hard_limits(valid_off, travler)
    scored_offers, score_details = weights_score(pass_hl_offers, travler)
    top_offers = rank_offers(scored_offers)

    if not top_offers:
        print("no offers match your choices")
        return None



    offer_by_id= {o.offer_id: o for o in pass_hl_offers}
    for number, (offer_id, score) in enumerate(top_offers,start=1):
        seats=offer_by_id[offer_id].seats_available
        print(f"{number}. {offer_id}: {score:.1f} ({seats} seats left)")
    best_id=top_offers[0][0]
    explain_top_offer(best_id,score_details[best_id], travler.weights, number)


    while True:
        choice=input("enter the number of the offer you are choosing (or '+' for more details): ")

        if choice == "+":
            for offer_id, score in top_offers:
                print(f"{offer_id} total{score:.1f}")
                for name, part in score_details[offer_id].items():
                    print(f" ---- {name}: {part:.1f}")
            continue



        if choice.isdigit() and 1<= int(choice) <=len(top_offers):
            break
        print("invalid choice")

            
    chosen_id=top_offers[int(choice)-1][0]
    for offer in pass_hl_offers:
        if offer.offer_id == chosen_id:
            return offer


def save_booking(booking):
    OUT_DIR.mkdir(exist_ok=True)
    file= OUT_DIR / "bookings.json"
    bookings=[]

    if file.exists():
        with open(file, encoding="utf-8") as f:
            bookings = json.load(f)
    offer = booking.chosen_offer
    bookings.append( {
        "booking_ref": booking.booking_ref,
        "booking_time":booking.booking_time.isoformat(),
        "offer_id": offer.offer_id,
        "price_eur": offer.price_eur,
        "changeable": offer.changeable,
        "refundable": offer.refundable,
    })

    with open(file, "w", encoding="utf-8") as f:
        json.dump(bookings, f, indent=4)




def book_offer(offer):
    if offer.seats_available <= 0:
        raise BookingError(offer.offer_id, "no seats")

    offer.seats_available= offer.seats_available - 1
    booking = Booking(chosen_offer=offer, booking_ref=make_booking_ref())
    if not BOOKING_REFERENCE_CODE.fullmatch(booking.booking_ref):
        raise BookingError(booking.booking_ref, "invalid booking refference format")
    booking_logger.info(f"booked {booking.booking_ref} on {offer.offer_id}")
    save_booking(booking)
    return booking
            





