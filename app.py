
import random
import streamlit as st

from poker import deal_hand, hand_notation
from strategy import OPEN_RANGES, best_action


# ------------------------------------------
# PAGE SETUP
# ------------------------------------------

st.set_page_config(
    page_title="PokerLab",
    page_icon="♠",
    layout="centered"
)

st.title("♠ PokerLab")
st.caption("6-Max Texas Hold'em Preflop Trainer")

# Use only positions with opening ranges
POSITIONS = list(OPEN_RANGES.keys())


# ------------------------------------------
# SESSION STATE
# ------------------------------------------

# Streamlit reruns the script when you interact
# with buttons, so session_state remembers data.

if "hand" not in st.session_state:
    st.session_state.hand = deal_hand()

if "position" not in st.session_state:
    st.session_state.position = random.choice(POSITIONS)

if "answer" not in st.session_state:
    st.session_state.answer = None

if "total" not in st.session_state:
    st.session_state.total = 0

if "correct" not in st.session_state:
    st.session_state.correct = 0

if "history" not in st.session_state:
    st.session_state.history = []


# ------------------------------------------
# FUNCTIONS
# ------------------------------------------

def new_hand():
    st.session_state.hand = deal_hand()
    st.session_state.position = random.choice(POSITIONS)
    st.session_state.answer = None


def submit_answer(action):
    if st.session_state.answer is not None:
        return

    hand = st.session_state.hand
    position = st.session_state.position
    notation = hand_notation(hand)

    correct_action = best_action(position, notation)
    is_correct = action == correct_action

    st.session_state.answer = action
    st.session_state.total += 1

    if is_correct:
        st.session_state.correct += 1

    st.session_state.history.append({
        "hand": notation,
        "position": position,
        "your_action": action,
        "correct_action": correct_action,
        "correct": is_correct
    })


# ------------------------------------------
# DISPLAY CURRENT HAND
# ------------------------------------------

hand = st.session_state.hand
position = st.session_state.position
notation = hand_notation(hand)

SUIT_SYMBOLS = {
    "s": "♠",
    "h": "♥",
    "d": "♦",
    "c": "♣"
}


def display_card(card):
    rank = card[0]
    suit = SUIT_SYMBOLS[card[1]]
    return rank + suit


card1 = display_card(hand[0])
card2 = display_card(hand[1])

st.subheader("Your Hand")

col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    st.markdown(f"### {card1}")

with col2:
    st.markdown(f"### {card2}")

with col3:
    st.write(f"**Position:** {position}")
    st.write("**Stack:** 100 BB")

st.info("Everyone folds to you. What's your move?")


# ------------------------------------------
# DECISION BUTTONS
# ------------------------------------------

if st.session_state.answer is None:

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "Fold",
            use_container_width=True
        ):
            submit_answer("fold")
            st.rerun()

    with col2:
        if st.button(
            "Raise",
            use_container_width=True
        ):
            submit_answer("raise")
            st.rerun()

else:

    correct_action = best_action(position, notation)
    your_action = st.session_state.answer

    if your_action == correct_action:
        st.success("Correct decision!")
    else:
        st.error("Incorrect decision!")

    st.write(f"**Your hand:** {notation}")
    st.write(f"**Your action:** {your_action}")
    st.write(f"**Reference action:** {correct_action}")

    if correct_action == "raise":
        st.write(
            f"{notation} belongs to the opening "
            f"range from {position}."
        )
    else:
        st.write(
            f"{notation} is outside the standard "
            f"opening range from {position}."
        )

    if st.button(
        "Next Hand",
        use_container_width=True
    ):
        new_hand()
        st.rerun()


# ------------------------------------------
# OVERALL PERFORMANCE
# ------------------------------------------

st.divider()
st.subheader("Your Statistics")

total = st.session_state.total
correct = st.session_state.correct

accuracy = correct / total if total else 0

col1, col2, col3 = st.columns(3)

col1.metric("Hands Practiced", total)
col2.metric("Correct", correct)
col3.metric("Accuracy", f"{accuracy:.1%}")


# ------------------------------------------
# PERFORMANCE BY POSITION
# ------------------------------------------

st.subheader("Accuracy by Position")

for pos in POSITIONS:

    attempts = [
        entry for entry in st.session_state.history
        if entry["position"] == pos
    ]

    if not attempts:
        st.write(f"{pos}: No hands practiced")
        continue

    correct_count = sum(
        entry["correct"] for entry in attempts
    )

    pos_accuracy = correct_count / len(attempts)

    st.write(
        f"**{pos}:** {pos_accuracy:.1%} "
        f"({correct_count}/{len(attempts)})"
    )

    st.progress(pos_accuracy)


# ------------------------------------------
# HAND HISTORY
# ------------------------------------------

with st.expander("View Hand History"):

    if st.session_state.history:
        st.dataframe(
            st.session_state.history,
            use_container_width=True
        )
    else:
        st.write("No hands practiced yet.")


# ------------------------------------------
# RESET BUTTON
# ------------------------------------------

if st.button("Reset Statistics"):
    st.session_state.total = 0
    st.session_state.correct = 0
    st.session_state.history = []
    new_hand()
    st.rerun()
