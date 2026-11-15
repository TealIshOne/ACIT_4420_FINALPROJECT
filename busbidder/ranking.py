


def rank_offers(scored_offers):
    """
    ranks offers based on their scores and returns a sorted list of offers.
    """
    sorted_offers = sorted(scored_offers.items(), key=lambda x: x[1], reverse=True)
    top_offers =[offer for offer in sorted_offers[:5]]
    return top_offers
