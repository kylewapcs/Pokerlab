import random

RANKS = "23456789TJQKA"
suits = "cshd"

def create_deck():
    deck = []
    for i in range(13):
        for j in range(4):
            deck.append(RANKS[i] + suits[j])
    random.shuffle(deck)
    return deck

def deal_hand():
    deck = create_deck()
    return deck[:2]


def hand_notation(hand):
    card1, card2 = hand
    rank1, rank2 = card1[0], card2[0]
    suit1, suit2  = card1[1], card2[1]
    if rank1 == rank2:
        return rank1 + rank2
    high, low = sorted(
        [rank1, rank2],
        key=lambda rank: RANKS.index(rank),
        reverse=True)

    return high + low + ("s" if suit1 == suit2 else "o")

if __name__ == "__main__":
    hand = deal_hand()
    print("Dealt hand:", hand)
    print("Hand notation:", hand_notation(hand))