from busbidder.validation import validate_offers
from busbidder.loader import call_files
import json
import csv 
from pathlib import Path

PROF_DIR=Path("config")
CSV_DIR=Path("data")

# files=[
#     PROF_DIR/"profiles.json",
#     CSV_DIR/"companies.csv",
#     CSV_DIR/"destinations.csv",
#     CSV_DIR/"offers_bad.csv",
#     CSV_DIR/"offers.csv"
# ]


# files=call_files(["bad"])



# def test_rows(files):
#     '''
#     due to the way the offers_bad.csv file is set up we can do a standard run through of the full file,
#       eahc row should fail at different check points, except one, as it needs to be tested with the offers.csv
#       to catch duplicates
#     '''

files = call_files(["bad"])

def test_bad_file():
    valid, reject = validate_offers(files["bad"])
    for row, reason in reject:                      # MOVED up
        print(reason)
    print([offer.offer_id for offer in valid])      # MOVED up
    assert len(reject) == 13
    assert len(valid) == 1






