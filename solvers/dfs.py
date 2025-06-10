from utils.puzzle_utils_1 import find_blank, swap, get_neighbors

def dfs(initial_state, goal_state):
    stack = [(initial_state, 0)]
    visited = set([initial_state])
    parent_map = {initial_state: None}
    nodes_explored = 0

    while stack:
        current_state, depth = stack.pop()
        nodes_explored += 1

        if current_state == goal_state:
            path = []
            while current_state:
                path.append(current_state)
                current_state = parent_map[current_state]
            return path[::-1], nodes_explored

        for neighbor in get_neighbors(current_state):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append((neighbor, depth + 1))
                parent_map[neighbor] = current_state

    return None, nodes_explored
