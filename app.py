import streamlit as st
import random
import time
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Memory Match", page_icon="🧠")
st.title("🧠 Memory Card Matching")
st.write("Find all 8 matching pairs! You have 10 wrong attempts before a new game auto-starts.")

SYMBOLS = ["🍎", "🍌", "🍇", "🍉", "🍒", "🍑", "🍍", "🥝"]
MOTIVATIONAL_PHRASES = [
    "🌟 Amazing memory! You crushed it!",
    "🔥 You're on fire! Incredible focus!",
    "🏆 Champion mindset! Well played!",
    "💪 Sharp as ever! Great job!",
    "🎯 Perfect focus! That was clean!",
    "✨ Brilliant work! Memory master!",
]

def new_game():
    cards = SYMBOLS * 2
    random.shuffle(cards)
    st.session_state.cards = cards
    st.session_state.matched = set()
    st.session_state.flipped = []
    st.session_state.moves = 0
    st.session_state.wrong_attempts = 0
    st.session_state.win_shown = False
    st.session_state.mismatch_time = None  # NEW: tracks when a mismatch happened

if "cards" not in st.session_state:
    new_game()

def handle_card_click(i):
    # NEW: block clicks while a mismatch is being shown (mimics the old "frozen" pause, but responsively)
    if st.session_state.mismatch_time is not None:
        return
    if len(st.session_state.flipped) >= 2:
        return
    if i in st.session_state.matched or i in st.session_state.flipped:
        return
    st.session_state.flipped.append(i)
    if len(st.session_state.flipped) == 2:
        st.session_state.moves += 1

@st.dialog("😔 Better luck next time!")
def fail_popup():
    st.write("You've reached 10 wrong attempts. Let's try again!")
    if st.button("OK, New Game"):
        new_game()
        st.rerun()

@st.dialog("🎉 You Won!")
def win_popup():
    st.write(random.choice(MOTIVATIONAL_PHRASES))
    if st.button("Play Again"):
        new_game()
        st.rerun()

st.write(f"**Moves:** {st.session_state.moves}  |  **Wrong attempts:** {st.session_state.wrong_attempts}/10")

for row in range(4):
    cols = st.columns(4)
    for col in range(4):
        i = row * 4 + col
        is_visible = i in st.session_state.matched or i in st.session_state.flipped
        label = st.session_state.cards[i] if is_visible else "🎴"
        disabled = i in st.session_state.matched
        if cols[col].button(label, key=f"card_{i}", use_container_width=True, disabled=disabled):
            handle_card_click(i)

# Check the 2 flipped cards AFTER drawing the board, so the player sees them first
if len(st.session_state.flipped) == 2 and st.session_state.mismatch_time is None:
    a, b = st.session_state.flipped
    if st.session_state.cards[a] == st.session_state.cards[b]:
        st.session_state.matched.add(a)
        st.session_state.matched.add(b)
        st.session_state.flipped = []
    else:
        st.session_state.mismatch_time = time.time()  # NEW: mark the moment, don't sleep

# NEW: non-blocking check — has 1 second passed since the mismatch?
if st.session_state.mismatch_time is not None:
    if time.time() - st.session_state.mismatch_time >= 1:
        st.session_state.flipped = []
        st.session_state.wrong_attempts += 1
