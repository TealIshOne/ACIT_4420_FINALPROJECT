'''
this file will load all datafiles (json, csv)
'''

import json
import csv 
from pathlib import Path

from busbidder.errors import InvalidFileError

BASE_DIR=Path(__file__).resolve().parent.parent 
PROF_DIR=BASE_DIR/"config"
CSV_DIR=BASE_DIR/"data"



def call_files(call_key_list=None):
    VALID_KEYS=["prof", "comp", "dest", "bad", "off"]
    results={}

    good_keys=[]

    if call_key_list is None:
        raise ValueError("call_files needs a list of keys")

    for item in call_key_list:
        if item  in VALID_KEYS:
            good_keys.append(item)

    call_key_list=good_keys      

    if len(call_key_list) == 0: 
        raise ValueError("call_files needs a list of keys")

    if "prof" in call_key_list:
        try:
            with open(PROF_DIR/"profiles.json", encoding="utf-8") as f:
                results["prof"] = json.load(f)
        except FileNotFoundError as err:
            missing=Path(err.filename)
            raise InvalidFileError(missing.parent, missing.name) from err
        except json.JSONDecodeError as err:
            raise InvalidFileError(PROF_DIR, "profiles.json, broken file") from err


    if "comp" in call_key_list:
        try:
            with open(CSV_DIR / "companies.csv", newline="", encoding="utf-8") as f: 
                results["comp"] = list(csv.DictReader(f))
        except FileNotFoundError as err:
            missing=Path(err.filename)
            raise InvalidFileError(missing.parent, missing.name) from err
        

    if "dest" in call_key_list:
        try:
            with open(CSV_DIR / "destinations.csv", newline="", encoding="utf-8") as f: 
                results["dest"] = list(csv.DictReader(f))
        except FileNotFoundError as err:
            missing=Path(err.filename)
            raise InvalidFileError(missing.parent, missing.name) from err

    if "bad" in call_key_list:
        try:
            with open(CSV_DIR / "offers_bad.csv", newline="", encoding="utf-8") as f: 
                results["bad"] = list(csv.DictReader(f))
        except FileNotFoundError as err:
            missing=Path(err.filename)
            raise InvalidFileError(missing.parent, missing.name) from err

    if "off" in call_key_list:
        try:
            with open(CSV_DIR / "offers.csv", newline="", encoding="utf-8") as f: 
                results["off"] = list(csv.DictReader(f))
        except FileNotFoundError as err:
            missing=Path(err.filename)
            raise InvalidFileError(missing.parent, missing.name) from err

    return results



