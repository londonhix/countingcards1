def card_value(card):
    if card in ['2', '3', '4', '5', '6']:
        return 1
    elif card in ['7', '8', '9']:
        return 0
    else:
        return -1

def betting_advice(count):
    if count >= 2:
        return 'Bet Big'
    elif count <= 0:
        return 'Bet Small'
    else:
        return 'Bet Neutral'
