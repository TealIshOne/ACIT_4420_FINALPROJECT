import logging

logging.basicConfig(
    filename="logs/busbidder_rejects.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


from busbidder.loader import call_files           
from busbidder.validation import validate_offers   

files = call_files(["bad"])                        