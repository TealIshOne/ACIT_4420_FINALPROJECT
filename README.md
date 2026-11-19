python -m venv .venv

.venv\Scripts\python -m pip install -r
requirements.txt

| Candidate_nr | Class    | date       |
| ------------ | -------- | ---------- |
| 870          | ACIT4420 | 20.11.2026 |

# BusBidder

The Code is a  modulised simulation of a buss travle booking system using hardcoded CSV and JSON data files.

The program uses the datafiles to valdiate, filter and rate  travle offers based on user inputs into a travle profile

**Breakdown of program function:**

1. loads companies, destinations, offers, and traveler profiles
2. requests, checks and validates all input data, and prompts user for a predetermiend travle profile with the oportunity to request more info on the profile (datafiles and user input)
3. removes offers that break with ruels (filter)
4. scores the rest of the offers with weight (ranking), provides user with maximum top 5 offers if more are aplicable
5. shows the user the ranked list with the choice to request more information of requirement scores
6. lets the travle book offerts/ change travle profile and logs data without exiting and restarting program.
7. exiting program can be done in 'start' menue by hititng corresponding key, or at any point with keyboardinterupt.

# Requirments

- Python 3.14
- Libraries: see requriemnt.txt

# Setup

Only standard libraries, pluss pytest for test cases

# Run

**Cloning git repository:**

```Python
git clone https://github.com/TealIshOne/ACIT_4420_FINALPROJECT.git

cd ACIT_4420_FINALPROJECT

python -m venv .venv

.venv\Scripts\python -m pip install -r requirements.txt
```

**From the project folder:**

```Python
python -m busbidder
```

# Tests

```Python
python -m pytest -v
```

# Input Files

the input files used for the code are found in the  and \data and \config directories and are named the following:

config\profiles.json 	// this file contains the travler profies the user can choose between when booking

data\companies.csv	// this file contains the available copanies and their company id

data\destinations.csv	// this file contains the available destinations and their destination id

data\offers_bad.csv		// this file contains only bad offers, meaning they should be filtered out through validation

data\offers.csv			// this file contains only good offers, meaning they should all remaina after validation

# Output Files

the code has two logging/output directories, one is \logs with data provided through logger functions and \outputs containing manual logging of bookings

outputs\bookings.json	// every booking performed by the user is logged in this output file with relelvant booking information

logs\booking.log		//this log file also logs bookings, however provides realtime data of booking time, and fewer relevant datapoints

logs\bussbidder_reject_offers.log	// this function stores rejected (bad) offers after validation

logs\busbidder.log		// this log file takes only crash warnings for missing files as defined in main

# Limitations

1. One major limitation is the limited number of offers given in offers.csv. This mean  the user may find it difficult to find an available offer if they are not familiar with the available offers. The offers available remain between July 12 2026 and July 14 2026.
2. One  of the main limitations of the system is that the user can only book one seat/offer at a time, however the program is not destigned for group bookings.
3. There is no way to cancel or change a booking once it is chosen, and payment is simulated.
4. Seats are counted in program and are not changed in the datafiles. The seat count is stored in outputs/bookings.json, so if this file is deleated the seats return to default based ont eh datafiles.
5. One destination per booking, multi-city travle is not an option.
6. Travler profiles are fixed and cannot be changed in program, can only be changed by ammending the file itself.
7. valid destinations and company ids are hardcoed in validation.py, a new destination therefore needs a code change in adition to a datafile change.
8. Stars (customer_rating) is checked but never used in the scoring
9. 'Flexibility only looks at 'changable' not 'refundable'
10. only top 5 offers are shown, this limits the users choices. Thos value was chosen for readability and is a single digit code change.

# Possible unfair outcomes

1. **Scores are relative**: prices, duration and CO2 are scaled between min/max of the remaining offer. so an offers score can drop just because a cheaper one exists. A high score is relevant to other offers, not a general score. if all offers are the same they are given 0 points.
2. **Departure time uses a fixed 24-hour scalr**e: while the rest of the parameters are relative, so its counted a bit different than the rest.
3. **Hard Limits are Strict:** if a hard limit is £30, a price of £30.01 would be ecluded form final offer conciderations
4. **Flexibility is all or nothong**: eithe full score or 0, this may negatively/poositively affect the final scoring even if not strictly relevant
5. **Companies with many offers**: gets an advantage in reaching top 5 scores as they have more oprotuneties.
