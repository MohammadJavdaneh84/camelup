import streamlit as st
from PIL import Image

st.set_page_config(layout="wide")

# Initial session state if not present
if "board" not in st.session_state:
    st.session_state.board = [[] for _ in range(16)]  # 16 columns

# Colors to represent camels
camel_colors = ["red", "blue", "yellow", "green", "white"]

# Mapping for displaying trap types
trap_display = {"pond": "pond", "desert": "desert"}
trap_cycle = {"pond": "desert", "desert": None, None: "pond"}

def render_board():
    cols = st.columns(16)
    max_height = max(len(stack) for stack in st.session_state.board)
    for row in range(max_height, 0, -1):
        for i in range(16):
            with cols[i]:
                if len(st.session_state.board[i]) >= row:
                    item = st.session_state.board[i][row - 1]
                    if item in camel_colors:
                        st.markdown(f"<div style='background-color:{item};width:100%;height:40px;border:1px solid black'></div>", unsafe_allow_html=True)
                    elif item in trap_display:
                        st.markdown(f"<div style='background-color:lightgrey;width:100%;height:40px;border:1px solid black;text-align:center;'>{item}</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='height:40px;border:1px solid #ccc'></div>", unsafe_allow_html=True)

    # Plus buttons
    for i in range(16):
        with cols[i]:
            if st.button("➕", key=f"add_{i}"):
                handle_column_click(i)

def handle_column_click(i):
    stack = st.session_state.board[i]
    if not stack:
        choice = st.radio("اضافه کردن به خانه خالی:", camel_colors + ["pond", "desert"], key=f"choice_{i}")
        if st.button("ثبت", key=f"confirm_{i}"):
            stack.insert(0, choice)
    elif stack[0] in trap_display:
        current_trap = stack[0]
        new_trap = trap_cycle[current_trap]
        if new_trap:
            stack[0] = new_trap
        else:
            stack.pop(0)
    elif stack[0] in camel_colors:
        choice = st.radio("شتر جدید اضافه کن:", camel_colors, key=f"newcamel_{i}")
        if st.button("اضافه", key=f"addcamel_{i}"):
            # remove from other columns if exists
            for j in range(16):
                if i != j and choice in st.session_state.board[j]:
                    idx = st.session_state.board[j].index(choice)
                    st.session_state.board[j].pop(idx)
                    # move upper camels down
                    for move_idx in range(idx, len(st.session_state.board[j])):
                        if move_idx + 1 < len(st.session_state.board[j]):
                            st.session_state.board[j][move_idx] = st.session_state.board[j][move_idx + 1]
                    break
            stack.insert(0, choice)

# Render UI
title_cols = st.columns(16)
for i in range(16):
    with title_cols[i]:
        st.markdown(f"<h5 style='text-align:center'>{i+1}</h5>", unsafe_allow_html=True)

render_board()
