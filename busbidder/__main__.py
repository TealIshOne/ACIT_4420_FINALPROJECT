import logging
from busbidder.menu import menu
from busbidder.errors import BusBidderError
from pathlib import Path


LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
                             

logging.basicConfig(
    filename=LOG_DIR/"busbidder.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)



rejects_logger = logging.getLogger("rejects")
rejects_handler = logging.FileHandler(LOG_DIR/"busbidder_reject_offers.log", encoding="utf-8")
rejects_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
rejects_logger.addHandler(rejects_handler)
rejects_logger.propagate=False


booking_logger=logging.getLogger("bookings")
booking_handler=logging.FileHandler(LOG_DIR/"booking.log", encoding="utf-8")
booking_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
booking_logger.addHandler(booking_handler)
booking_logger.propagate=False



if __name__ == "__main__":  
    try:             
        menu() 
    except BusBidderError as err:
        print(f"sorry, the program has stopped: {err}")
        logging.error(err)
    except (KeyboardInterrupt, EOFError):
        print("GOODBYE!")

    except Exception as err:
        print("sorry, something unexpected went wrong, see logs/busbidder.log")
        logging.exception(err)

