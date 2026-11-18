


def explain_top_offer(offer_id, details, weights, nr):

    shares = {name: part/weights[name] for name, part in details.items() if weights[name]>0}
    best= max(shares, key=lambda name: (shares[name], weights[name]))
    weakest= min(shares, key=lambda name: (shares[name], -weights[name]))

    print(f"\nWhy {offer_id} is nr. {nr}: ")
    print(f" strongest: {best} ({shares[best]:.2f} of full points)")
    print(f" weakest: {weakest} ({shares[weakest]:.2f} of full points)\n")