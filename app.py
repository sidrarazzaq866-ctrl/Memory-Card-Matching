import streamlit as st
import random

st.set_page_config(page_title="Memory Match", page_icon="🧠")
st.title("🧠 Memory Card Matching")
st.write("Find all 8 matching pairs in as few moves as possible!")

SYMBOLS = ["🍎", "🍌", "🍇", "🍉", "🍒", "🍑", "🍍", "🥝"]

def new_game():
    cards = SYMBOLS * 2
    random.shuffle(cards)
    st.session_state.cards = cards
    st.session_state.matched = set()
    st.session_state.flipped = []
    st.session_state.moves = 0
    st.session_state.mismatch_pending = False

if "cards" not in st.session_state:
    new_game()

def handle_card_click(i):
    if st.session_state.mismatch_pending:
        return  # must click Continue first
    if i in st.session_state.matched or i in st.session_state.flipped:
        return  # already matched or already flipped

    st.session_state.flipped.append(i)

    if len(st.session_state.flipped) == 2:
        st.session_state.moves += 1
        a, b = st.session_state.flipped
        if st.session_state.cards[a] == st.session_state.cards[b]:
            st.session_state.matched.add(a)
            st.session_state.matched.add(b)
            st.session_state.flipped = []
        else:
            st.session_state.mismatch_pending = True  # wait for Continue

def clear_mismatch():
    st.session_state.flipped = []
    st.session_state.mismatch_pending = False

st.write(f"**Moves:** {st.session_state.moves}")

for row in range(4):
    cols = st.columns(4)
    for col in range(4):
        i = row * 4 + col
        is_visible = i in st.session_state.matched or i in st.session_state.flipped
        label = st.session_state.cards[i] if is_visible else "🎴"
        disabled = i in st.session_state.matched
        if cols[col].button(label, key=f"card_{i}", use_container_width=True, disabled=disabled):
            handle_card_click(i)
            st.rerun()

if st.session_state.mismatch_pending:
    st.warning("Not a match! Click Continue to flip them back.")
    if st.button("Continue"):
        clear_mismatch()
        st.rerun()

if len(st.session_state.matched) == len(st.session_state.cards):
    st.success(f"🎉 You matched all pairs in {st.session_state.moves} moves!")

if st.button("🔄 New Game"):
    new_game()
    st.rerun()
