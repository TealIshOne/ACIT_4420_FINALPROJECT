
from busbidder.models import Offer, Traveller
from datetime import datetime

## ---offer should come from valid after validation, traveller should come from the traveller class

def map_to_unit(value, min_value, max_value):
    """
    Maps a value to a unit scale between 0 and 1 based on the provided min and max values.
    """
    if max_value == min_value:
        return 0.0  # Avoid division by zero; return 0 if min and max are the same
    return (value - min_value) / (max_value - min_value)

def passes_hard_limits(offers, traveller):
    """
    Filters offers based on the traveller's hard limits.
    """
    offers_passed=[]
    for key, limit in traveller.hard_limits.items():
        if limit is None:   
            continue 
        if key == "max_price_eur":
            passed  = [offer for offer in offers if offer.price_eur <= limit]
            offers_passed.append(passed)
        elif key == "max_transfers":
            passed = [offer for offer in offers if offer.transfers <= limit]
            offers_passed.append(passed)
        elif key == "min_luggage_kg":
            passed  = [offer for offer in offers if offer.luggage_kg >= limit]
            offers_passed.append(passed)
        elif key == "changeable_required":
            if limit:
                passed = [offer for offer in offers if offer.changeable]
                offers_passed.append(passed)

    if not offers_passed:
        return offers
    hard_limits_passed = list(set.intersection(*map(set, offers_passed)))
    return hard_limits_passed





def weights_score(offers, traveller):
    """
    Filters offers based on the traveller's weights.
    uses offers from hard limits filter, and weights from traveller class
    """
    if not traveller.weights:
        return {}

    weighted_offers = {}
    durations = [offer.duration_min for offer in offers]
    co2_values = [offer.co2_kg for offer in offers]
    prices = [offer.price_eur for offer in offers]

    for offer in offers:
        score = 0
        for key, weight in traveller.weights.items():
            if key == "price":
                score += (1 - map_to_unit(offer.price_eur, min(prices), max(prices))) * weight
            elif key == "flexibility":
                score += (1 if offer.changeable else 0) * weight
            elif key == "duration":
                score += (1- map_to_unit(offer.duration_min, min(durations), max(durations))) * weight
            elif key == "co2":
                score += (1 - map_to_unit(offer.co2_kg, min(co2_values), max(co2_values))) * weight
            elif key == "departure_time":
                date_str = offer.departure.strftime("%Y/%m/%d") 
                preferred_departure_time = datetime.strptime(date_str + " " + traveller.preferred_departure, "%Y/%m/%d %H:%M")
                gap=abs((preferred_departure_time - offer.departure).total_seconds())/60

                score += (1-map_to_unit(gap, 0, 1440)) * weight
        weighted_offers[offer.offer_id] = score


    return weighted_offers