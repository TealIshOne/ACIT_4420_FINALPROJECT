

from busbidder.loader import call_files
from busbidder.models import Traveller
from busbidder.validation import validate_offers
from datetime import datetime


menu_start=[
    "1. add a traveller profile",
    "2. Book a trip",
    "3. Exit"
]


def menu():
    for item in menu_start:
        print(item)

    choice = input("Choose an option (1-3): ")
    if choice == "1":
        '''
        here the user chooses a predetermined traveller profile from the config folder, 
        or creates a new one. and add preferred departure time. 
        the profile is then saved to the config folder as a json file.
        '''
        pass
    if choice == "2":
        '''
        here the top five travle offers are printed to the user,
        based on the traveller profile and the offers in the data folder. 
        the user can then choose to book one of the offers, or go back to the main menu.
        '''
        pass
    if choice == "3":
        print("Exiting the program.")
        exit()

