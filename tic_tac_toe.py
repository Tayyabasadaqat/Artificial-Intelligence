import streamlit as st
import random

st.set_page_config(
    page_title="Tic Tac Toe",
    page_icon="⭕",
    layout="centered"
)

# -------------------------
# Initialize Session State
# -------------------------
if "board" not in st.session_state:
    st.session_state.board = [""] * 9

if "current_player" not in st.session_state:
    st.session_state.current_player = "X"

if "winner" not in st.session_state:
    st.session_state.winner = None

if "game_over" not in st.session_state:
    st.session_state.game_over = False

if "mode" not in st.session_state:
    st.session_state.mode = "Player vs Player"

if "score_x" not in st.session_state:
    st.session_state.score_x = 0

if "score_o" not in st.session_state:
    st.session_state.score_o = 0

if "draws" not in st.session_state:
    st.session_state.draws = 0


# -------------------------
# Functions
# -------------------------

winning_combinations = [
    (0,1,2),
    (3,4,5),
    (6,7,8),
    (0,3,6),
    (1,4,7),
    (2,5,8),
    (0,4,8),
    (2,4,6)
]


def check_winner(board):

    for combo in winning_combinations:
        a,b,c = combo

        if board[a] == board[b] == board[c] != "":
            return board[a]

    if "" not in board:
        return "Draw"

    return None


def reset_board():
    st.session_state.board = [""] * 9
    st.session_state.current_player = "X"
    st.session_state.game_over = False
    st.session_state.winner = None


def ai_move():

    empty = [i for i,v in enumerate(st.session_state.board) if v == ""]

    if empty:
        choice = random.choice(empty)
        st.session_state.board[choice] = "O"

        result = check_winner(st.session_state.board)

        if result:
            st.session_state.game_over = True
            st.session_state.winner = result

            if result == "X":
                st.session_state.score_x += 1
            elif result == "O":
                st.session_state.score_o += 1
            else:
                st.session_state.draws += 1

        else:
            st.session_state.current_player = "X"


def player_move(index):

    if st.session_state.board[index] == "" and not st.session_state.game_over:

        st.session_state.board[index] = st.session_state.current_player

        result = check_winner(st.session_state.board)

        if result:

            st.session_state.game_over = True
            st.session_state.winner = result

            if result == "X":
                st.session_state.score_x += 1

            elif result == "O":
                st.session_state.score_o += 1

            else:
                st.session_state.draws += 1

        else:

            if st.session_state.mode == "Player vs Computer":

                st.session_state.current_player = "O"
                ai_move()

            else:

                st.session_state.current_player = (
                    "O"
                    if st.session_state.current_player == "X"
                    else "X"
                )


# -------------------------
# Sidebar
# -------------------------

st.sidebar.title("⚙️ Settings")

mode = st.sidebar.radio(
    "Game Mode",
    ["Player vs Player", "Player vs Computer"]
)

if mode != st.session_state.mode:
    st.session_state.mode = mode
    reset_board()

st.sidebar.markdown("---")

st.sidebar.subheader("🏆 Scoreboard")

st.sidebar.write(f"❌ Player X : **{st.session_state.score_x}**")
st.sidebar.write(f"⭕ Player O : **{st.session_state.score_o}**")
st.sidebar.write(f"🤝 Draws : **{st.session_state.draws}**")

if st.sidebar.button("🔄 Reset Game"):
    reset_board()

if st.sidebar.button("🗑 Reset Scores"):
    st.session_state.score_x = 0
    st.session_state.score_o = 0
    st.session_state.draws = 0


# -------------------------
# Title
# -------------------------

st.title("⭕ Tic Tac Toe")

st.markdown("### Modern Streamlit Tic Tac Toe")

if not st.session_state.game_over:
    st.info(f"Current Turn: **{st.session_state.current_player}**")

else:

    if st.session_state.winner == "Draw":
        st.warning("🤝 It's a Draw!")

    else:
        st.success(f"🎉 Winner is {st.session_state.winner}")


# -------------------------
# Game Board
# -------------------------

for row in range(3):

    cols = st.columns(3)

    for col in range(3):

        index = row * 3 + col

        with cols[col]:

            label = st.session_state.board[index]

            if label == "":
                label = " "

            st.button(
                label,
                key=index,
                use_container_width=True,
                on_click=player_move,
                args=(index,)
            )


st.markdown("---")

col1, col2 = st.columns(2)

with col1:

    if st.button("New Round", use_container_width=True):
        reset_board()

with col2:

    if st.button("Exit Message", use_container_width=True):
        st.success("Thanks for playing! ❤️")

st.markdown("---")

st.caption("Made with ❤️ using Streamlit")