



from busbidder.booking_travler_info import Travlers_choices, booking_choices, book_offer
from busbidder.errors import BookingError



menu_start=[
    "1. add a traveller profile",
    "2. Book a trip",
    "3. Exit"
]


def menu():
    traveller  = None

    while True:

        for item in menu_start:
            print(item)

        choice = input(f"Choose an option (1-{len(menu_start)}): ")
        if choice == "1":
            '''
            TRAVLER PROFILE
            here the user chooses a predetermined traveller profile from the config folder, 
            or creates a new one. and add preferred departure time. 
            the profile is then saved to the config folder as a json file.
            '''
            traveller =Travlers_choices()



        elif choice == "2":
            '''
            BOOKING
            here the top five travle offers are printed to the user,
            based on the traveller profile and the offers in the data folder. 
            the user can then choose to book one of the offers, or go back to the main menu.
            '''
            if traveller is None:
                print("please choose a travle profile first (menu option 1)")
                continue
            chosen=booking_choices(traveller)
            if chosen is None:
                continue
            try:
                booking= book_offer(chosen)
                print(f"Booking confirmed! refference code: {booking.booking_ref}")
            except BookingError as err:
                print(f"sorry, booking failed: {err}")

        elif choice == "3":
            print("Exiting the program.")
            return 

        else:
            print(f"Invalid choice. Please enter a number between 1 and {len(menu_start)}.")



