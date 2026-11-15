import logging
from busbidder.models import Traveller
from busbidder.loader import call_files

traveller = Traveller.from_profile("budget", call_files(["prof"])["prof"])
print(traveller)
print(traveller.weights_ok(), traveller.hard_limits_ok(), traveller.departure_time_ok())

# logging.basicConfig(
#     filename="logs/busbidder_rejects.log",
#     level=logging.INFO,
#     format="%(asctime)s %(levelname)s %(message)s",
# )


# from busbidder.loader import call_files           
# from busbidder.validation import validate_offers   

# files = call_files(["bad"])                 TEST       



