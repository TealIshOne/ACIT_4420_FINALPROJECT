'''
this file will load all datafiles (json, csv)
'''

import json
import csv 
from pathlib import Path

PROF_DIR=Path("config")
CSV_DIR=Path("data")

files=[
    PROF_DIR/"profiles.json",
    CSV_DIR/"companies.csv",
    CSV_DIR/"destinations.csv",
    CSV_DIR/"offers_bad.csv",
    CSV_DIR/"offers.csv"
]


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
        with open(PROF_DIR/"profiles.json") as f:
            results["prof"] = json.load(f)

    if "comp" in call_key_list:
        with open(CSV_DIR / "companies.csv", newline="", encoding="utf-8") as f: 
            results["comp"] = list(csv.DictReader(f))

    if "dest" in call_key_list:
        with open(CSV_DIR / "destinations.csv", newline="", encoding="utf-8") as f: 
            results["dest"] = list(csv.DictReader(f))

    if "bad" in call_key_list:
        with open(CSV_DIR / "offers_bad.csv", newline="", encoding="utf-8") as f: 
            results["bad"] = list(csv.DictReader(f))

    if "off" in call_key_list:
        with open(CSV_DIR / "offers.csv", newline="", encoding="utf-8") as f: 
            results["off"] = list(csv.DictReader(f))

    return results

#print(call_files(["off", "xyz"]))

