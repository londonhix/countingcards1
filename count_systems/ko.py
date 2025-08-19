def card_value(card):
    # KO system treats all 2-7 as +1, 10s and Aces as -1
    if card in ['2', '3', '4', '5', '6', '7']:
        return 1
    elif card in ['10', 'J', 'Q', 'K', 'A']:
        return -1
    else:
        return 0

def betting_advice(count):
    if count >= 3:
        return 'Bet Big'
    elif count <= 0:
        return 'Bet Small'
    else:
        return 'Bet Moderate'
