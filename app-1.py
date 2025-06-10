import streamlit as st
import time
from PIL import Image
from solvers.a_star import a_star
from solvers.bfs import bfs
from solvers.dfs import dfs
from utils.puzzle_utils_1 import get_neighbors, get_move_direction
import base64
from io import BytesIO

GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)

# Must be first
st.set_page_config(page_title="8-Puzzle Solver", layout="centered")

# Optional layout padding cleanup
st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
for key, default in {
    "solution_path": [],
    "current_step": 0,
    "initial_state": GOAL_STATE,
    "tiles": [],
    "animation_done": False,
    "replay_requested": False,
    "replay_available": False,
    "just_solved": False
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# Function to animate solution
def animate_solution(path, tiles):
    placeholder = st.empty()
    for state in path:
        with placeholder.container():
            display_puzzle(state, tiles)
        time.sleep(0.5)


# Function to display puzzle grid
def display_puzzle(state, tiles=None, highlight_indices=None):
    if highlight_indices is None:
        highlight_indices = []

    st.markdown("""
        <style>
            .puzzle-grid {
                display: grid;
                grid-template-columns: repeat(3, 100px);
                grid-template-rows: repeat(3, 100px);
                gap: 0;
                justify-content: center;
                margin: 0 auto;
            }
            .puzzle-tile {
                width: 100px;
                height: 100px;
                border: 1px solid #ccc;
                display: flex;
                justify-content: center;
                align-items: center;
                box-sizing: border-box;
            }
            .puzzle-tile.highlight {
                border: 5px solid red;
            }
            .puzzle-tile img {
                width: 100px;
                height: 100px;
                display: block;
            }
        </style>
    """, unsafe_allow_html=True)

    grid_html = "<div class='puzzle-grid'>"
    for idx, val in enumerate(state):
        highlight_class = "highlight" if idx in highlight_indices else ""
        if val == 0:
            grid_html += f"<div class='puzzle-tile {highlight_class}' style='background-color: #f0f0f0;'></div>"
        else:
            if tiles:
                grid_html += (
                    f"<div class='puzzle-tile {highlight_class}'>"
                    f"<img src='data:image/png;base64,{tiles[val - 1]}' />"
                    f"</div>"
                )
            else:
                grid_html += f"<div class='puzzle-tile {highlight_class}'>{val}</div>"
    grid_html += "</div>"
    st.markdown(grid_html, unsafe_allow_html=True)


# Helpers to slice and convert image tiles
def image_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


def slice_image(image):
    image = image.resize((300, 300))
    tile_size = 100
    tiles = []
    for i in range(3):
        for j in range(3):
            left, upper = j * tile_size, i * tile_size
            right, lower = left + tile_size, upper + tile_size
            tile = image.crop((left, upper, right, lower))
            tiles.append(image_to_base64(tile))
    tiles[-1] = image_to_base64(Image.new("RGB", (100, 100), (255, 255, 255)))
    return tiles


# Shuffle puzzle
def shuffle_puzzle(state, moves=30):
    import random
    current_state = state
    for _ in range(moves):
        neighbors = get_neighbors(current_state)
        current_state = random.choice(neighbors)
    return current_state


# Main app
def main():
    st.title("🧩 8-Puzzle Solver with Step-by-Step Replay")

    algo = st.selectbox("Choose algorithm:", ["A*", "BFS", "DFS"])
    uploaded_file = st.file_uploader("Upload a square image (jpg, png)", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        if image.width != image.height:
            st.error("Please upload a square image.")
            return

        st.session_state.tiles = slice_image(image)

        if st.button("🔀 Shuffle Puzzle"):
            st.session_state.initial_state = shuffle_puzzle(GOAL_STATE)
            st.session_state.solution_path = []
            st.session_state.current_step = 0
            st.session_state.animation_done = False
            st.session_state.replay_available = False

        st.write("### Current Puzzle:")
        display_puzzle(st.session_state.initial_state, st.session_state.tiles)

        if st.button("🚀 Solve Puzzle"):
            st.write(f"Solving with {algo}...")
            init_state = st.session_state.initial_state
            if algo == "A*":
                path, explored = a_star(init_state, GOAL_STATE)
            elif algo == "BFS":
                path, explored = bfs(init_state, GOAL_STATE)
            else:
                path, explored = dfs(init_state, GOAL_STATE)

            if path:
                st.success(f"Solution in {len(path) - 1} moves! Nodes explored: {explored}")
                st.session_state.solution_path = path
                st.session_state.current_step = 0
                st.session_state.animation_done = False
                st.session_state.just_solved = True
            else:
                st.error(f"No solution found. Nodes explored: {explored}")

    if st.session_state.just_solved:
        animate_solution(st.session_state.solution_path, st.session_state.tiles)
        st.session_state.animation_done = True
        st.session_state.replay_available = True
        st.session_state.just_solved = False

    elif st.session_state.replay_requested:
        animate_solution(st.session_state.solution_path, st.session_state.tiles)
        st.session_state.replay_requested = False

    if st.session_state.solution_path and st.session_state.animation_done:
        if st.session_state.replay_available:
            if st.button("🔁 Replay Animation", key="replay_button_bottom"):
                st.session_state.replay_requested = True

        st.divider()
        st.markdown("### ▶️ Step-by-Step Puzzle Movement with Highlighted Tiles")

        path = st.session_state.solution_path
        current = st.session_state.current_step
        tiles = st.session_state.tiles
        highlight = []

        if current < len(path) - 1:
            arrow, r, c, from_idx, to_idx = get_move_direction(path[current], path[current + 1])
            highlight = [from_idx, to_idx]
        else:
            arrow = "✅"

        nav_col1, nav_col2, nav_col3, nav_col4 = st.columns([1, 2, 1, 1])
        with nav_col1:
            if current > 0 and st.button("⬅️ Back"):
                st.session_state.current_step -= 1
        with nav_col2:
            st.markdown(f"<div style='font-size:24px;text-align:center;'>Step {current} / {len(path) - 1}</div>",
                        unsafe_allow_html=True)
        with nav_col3:
            if current < len(path) - 1:
                if st.button(f"{arrow} Next"):
                    st.session_state.current_step += 1
            else:
                st.info("🎉 Puzzle Solved!")

        if current == len(path) - 1:
            st.balloons()

        display_puzzle(path[current], tiles, highlight_indices=highlight)

    elif not uploaded_file:
        st.info("Upload an image, shuffle, and solve to begin.")


if __name__ == "__main__":
    main()