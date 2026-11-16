


from busbidder.ranking import rank_offers
from busbidder.filters import passes_hard_limits, weights_score
from busbidder.models import  Traveller
from busbidder.loader import call_files

from busbidder.validation import validate_offers



files = call_files(["bad", "off", "prof"])
traveller = Traveller.from_profile("budget", files["prof"])

def test_ranking_order():
    """
    Checks if the offers are ranked in descending order based on their scores.
    """
    valid,rejected =validate_offers(files["off"]+files["bad"])
    filtered_offers = passes_hard_limits(valid, traveller)
    scored_offers, _= weights_score(filtered_offers, traveller)
    ranked_offers = rank_offers(scored_offers)
    scores = [score for offer_id, score in ranked_offers]


    assert scores == sorted(scores, reverse=True)
