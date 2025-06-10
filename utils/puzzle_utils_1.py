def find_blank(state):
    return state.index(0)

def swap(state, pos1, pos2):
    state = list(state)
    state[pos1], state[pos2] = state[pos2], state[pos1]
    return tuple(state)

def get_neighbors(state):
    neighbors = []
    blank_pos = find_blank(state)
    row, col = divmod(blank_pos, 3)

    moves = {
        "left": (row, col - 1),
        "right": (row, col + 1),
        "up": (row - 1, col),
        "down": (row + 1, col)
    }

    for new_row, new_col in moves.values():
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_blank = new_row * 3 + new_col
            new_state = list(state)
            new_state[blank_pos], new_state[new_blank] = new_state[new_blank], new_state[blank_pos]
            neighbors.append(tuple(new_state))
    return neighbors

def get_move_direction(from_state, to_state):
    blank_from = from_state.index(0)
    blank_to = to_state.index(0)
    r1, c1 = divmod(blank_from, 3)
    r2, c2 = divmod(blank_to, 3)

    if r1 == r2:
        direction = "←" if c1 > c2 else "→"
        return direction, r2, min(c1, c2), blank_from, blank_to
    elif c1 == c2:
        direction = "↑" if r1 > r2 else "↓"
        return direction, min(r1, r2), c2, blank_from, blank_to

    return "", 0, 0, blank_from, blank_to