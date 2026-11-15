from busbidder.ranking import rank_offers
from busbidder.filters import passes_hard_limits, weights_score
from busbidder.models import  Traveller
from busbidder.loader import call_files

from busbidder.validation import validate_offers

#### test profiles ###

no_limits = Traveller(
    profile_name="test_no_limits",
    hard_limits={"max_price_eur": None, "max_transfers": None,
                 "min_luggage_kg": None, "changeable_required": None},
    weights={"price": 100},
    preferred_departure="08:00",
)



files = call_files(["bad", "off", "prof"])
traveller = Traveller.from_profile("budget", files["prof"])

def test_budget_removes_too_expensive_offers():
    valid,rejected =validate_offers(files["off"]+files["bad"])
    filtered_offers = passes_hard_limits(valid, traveller)
    assert all(offer.price_eur <= traveller.hard_limits["max_price_eur"] for offer in filtered_offers)
    assert len(filtered_offers) < len(valid) and len(filtered_offers) > 0

def test_bad_profile_no_limits():
    valid,rejected =validate_offers(files["off"]+files["bad"])
    filtered_offers = passes_hard_limits(valid, no_limits)
    assert len(filtered_offers) == len(valid) and len(filtered_offers) > 0

def test_bad_offers_too_high_offer():
    valid,rejected =validate_offers(files["bad"])
    filtered_offers = passes_hard_limits(valid, traveller)
    assert len(filtered_offers) == 0
    assert len(valid) == 1

def test_empty_offers():
    filtered_offers = passes_hard_limits([], traveller)
    assert len(filtered_offers) == 0