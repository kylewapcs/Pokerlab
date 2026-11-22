
from poker import RANKS

POSITIONS = [
    "UTG",
    "HJ", "CO", "BTN", "SB"
]


def pocket_pairs(min_rank):
    start = RANKS.index(min_rank)
    return {rank * 2 for rank in RANKS[start:]}


def make_range(pairs, suited, offsuit):
    return (
        pocket_pairs(pairs)
        | set(suited.split())
        | set(offsuit.split())
    )


# Raise First In ranges from your screenshot.
# Assumes approximately 100 BB effective stacks with an ante.


OPEN_RANGES = {
    "UTG": make_range(
        "7",
        "AKs AQs AJs ATs A9s A8s A7s A6s A5s A4s A3s A2s "
        "KQs KJs KTs K9s K8s K7s "
        "QJs QTs Q9s "
        "JTs T9s",
        "AKo AQo AJo KQo"
    ),

    "HJ": make_range(
        "6",
        "AKs AQs AJs ATs A9s A8s A7s A6s A5s A4s A3s A2s "
        "KQs KJs KTs K9s K8s K7s K6s "
        "QJs QTs Q9s Q8s "
        "JTs J9s T9s",
        "AKo AQo AJo ATo "
        "KQo KJo KTo QJo"
    ),

    "CO": make_range(
        "4",
        "AKs AQs AJs ATs A9s A8s A7s A6s A5s A4s A3s A2s "
        "KQs KJs KTs K9s K8s K7s K6s K5s K4s "
        "QJs QTs Q9s Q8s "
        "JTs J9s J8s "
        "T9s T8s 98s 87s 76s",
        "AKo AQo AJo ATo A9o A8o "
        "KQo KJo KTo "
        "QJo QTo JTo"
    ),

    "BTN": make_range(
        "2",
        "AKs AQs AJs ATs A9s A8s A7s A6s A5s A4s A3s A2s "
        "KQs KJs KTs K9s K8s K7s K6s K5s K4s K3s K2s "
        "QJs QTs Q9s Q8s Q7s Q6s Q5s Q4s Q3s Q2s "
        "JTs J9s J8s J7s J6s J5s "
        "T9s T8s T7s T6s "
        "98s 97s 96s "
        "87s 86s "
        "76s 75s "
        "65s 64s 54s",
        "AKo AQo AJo ATo A9o A8o A7o A6o A5o A4o A3o "
        "KQo KJo KTo K9o K8o "
        "QJo QTo Q9o "
        "JTo J9o T9o"
    ),

    "SB": make_range(
        "2",
        "AKs AQs AJs ATs A9s A8s A7s A6s A5s A4s A3s A2s "
        "KQs KJs KTs K9s K8s K7s K6s K5s K4s K3s K2s "
        "QJs QTs Q9s Q8s Q7s Q6s Q5s Q4s Q3s Q2s "
        "JTs J9s J8s J7s J6s J5s "
        "T9s T8s T7s T6s "
        "98s 97s 96s "
        "87s 86s "
        "76s 75s "
        "65s 64s "
        "54s",
        "AKo AQo AJo ATo A9o A8o A7o A6o A5o A4o A3o "
        "KQo KJo KTo K9o K8o "
        "QJo QTo Q9o "
        "JTo J9o T9o"
    )
}


def best_action(position, hand):
    if hand in OPEN_RANGES[position]:
        return "raise"
    return "fold"

def count_combinations(hands):
    total = 0
    for hand in hands:
        if len(hand) == 2 and hand[0] == hand[1]:
            total += 6  # Pocket pair: 6 combinations
        elif len(hand) == 3 and hand[2] == 's':
            total += 4  # Suited: 4 combinations
        else:
            total += 12  # Offsuit: 12 combinations
    return total

def raise_frequency(position):
    hands = OPEN_RANGES[position]
    total_combinations = count_combinations(hands)
    return total_combinations / 1326  # Total combinations of two cards from a 52-card deck