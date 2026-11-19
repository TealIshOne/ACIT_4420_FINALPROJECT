import pytest
import busbidder.loader as loader
from busbidder.loader import call_files
from busbidder.validation import validate_offers
from busbidder.filters import passes_hard_limits
from busbidder.models import Traveller
from busbidder.errors import InvalidFileError

files = call_files(["off"])

def make_row(**changes):
    row = dict(files["off"][0])   # copy of the first good offer
    row.update(changes)
    return row


def test_stars_1_and_5():
    valid, rejected = validate_offers([make_row(stars="1"), make_row(offer_id="OF-8001", stars="5")])
    assert len(valid) ==2

def test_one_seat_kept_zero_rejections():
    valid, rejected = validate_offers([make_row(seats_available="1"), make_row(offer_id="OF-8001", seats_available="0")])
    assert len(valid) == 1 and len(rejected)==1



def test_exact_price():
    traveler=Traveller(profile_name="test_price_30", weights={'price':100}, 
                       preferred_departure="08:00", 
                       hard_limits={"max_price_eur": 30, "max_transfers": None,"min_luggage_kg": None, "changeable_required": None} )
    valid, rejected = validate_offers([make_row(price_eur="30")])
    assert len(passes_hard_limits(valid, traveler)) ==1

    


def test_load_sessions_missing_file():
    real_dir=loader.CSV_DIR
    loader.CSV_DIR=real_dir/ "non_existant_file"

    try:
        with pytest.raises(InvalidFileError):
            call_files(["off"])
    finally:
        loader.CSV_DIR = real_dir