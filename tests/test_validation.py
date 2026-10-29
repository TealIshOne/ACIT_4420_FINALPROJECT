from busbidder.validation import validate_offers
from busbidder.loader import call_files
import json
import csv 
from pathlib import Path

PROF_DIR=Path("config")
CSV_DIR=Path("data")



files = call_files(["bad", "off"])

def test_bad_file():
    valid, reject = validate_offers(files["bad"])
    for row, reason in reject:                     
        print(reason)
    print([offer.offer_id for offer in valid])    
    assert len(reject) == 13
    assert len(valid) == 1


print("-"*50)

def test_bad_file():
    valid, reject = validate_offers(files["off"])
    for row, reason in reject:                      
        print(reason)
    print([offer.offer_id for offer in valid])     
    assert len(reject) == 0
    assert len(valid) == 50

print("-"*50)

def test_both_files():
    valid, reject = validate_offers(files["off"] + files["bad"])
    for row, reason in reject:                      
        print(reason)
    print([offer.offer_id for offer in valid])     
    assert len(reject) == 14
    assert len(valid) == 50

