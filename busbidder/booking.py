# offer_id	company_id	destination_id	departure	arrival	duration_min	price_eur	transfers	luggage_kg	changeable	refundable	seats_available	rating	co2_kg




# traveler must be able to choose destination, data, a profile. changes to profile 



def ask_profile(profiles=None):
    if profiles is None:
        profiles = {}
    names=list(profiles)
    for number, name in enumerate(names, start=1):
        print(f"{number}. {profiles[name]['label']}")
    while True:
        choice =input("Choose a profile by number: ")
        if choice.isdigit() and 1 <= int(choice) <= len(names):
            return names[int(choice)-1]
        print("Invalid choice. Please enter a number corresponding to the profile.")


def ask_travel_requirements(requirements=None):
    req_list=[]
    if requirements is None:
        requirements = {}
    requirements_list = list(requirements.keys())
    for number, req in enumerate(requirements_list, start=1):
        print(f"{number}. {req}: {requirements[req]}")
    while True:
        choice = input("Choose a requirement by number: ")
        if choice.isdigit() and 1 <= int(choice) <= len(requirements_list):
            req_list.append(requirements_list[int(choice)-1])
            continue 
        if choice.lower() == "done":
            return req_list
        print("Invalid choice. Please enter a number corresponding to the requirement.")


def ask_destination(destinations=None):
    if destinations is None:
        destinations = []

    for number, dest in enumerate(destinations, start=1):
        print(f"{number}. {dest['destination_id']}: {dest['name']}")
    while True:
        choice = input("Choose a destination by number: ")
        if choice.isdigit() and 1 <= int(choice) <= len(destinations):
            return destinations[int(choice)-1]["destination_id"]
        print("Invalid choice. Please enter a number corresponding to the destination.")

def ask_departure_time(default_time=None):
    while True:
        time_input = input(f"Enter preferred departure time (HH:MM) [{default_time}]: ")
        if time_input == "":
            return default_time
        try:
            datetime.strptime(time_input, "%H:%M")
            return time_input
        except ValueError:
            print("Invalid time format. Please enter in HH:MM format.")