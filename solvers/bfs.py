from collections import deque
from utils.puzzle_utils_1 import find_blank, swap, get_neighbors

def bfs(initial_state, goal_state):
    queue = deque([(initial_state, 0)])
    visited = {initial_state}
    parent_map = {initial_state: None}
    nodes_explored = 0

    while queue:
        current_state, depth = queue.popleft()
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
                queue.append((neighbor, depth + 1))
                parent_map[neighbor] = current_state

    return None, nodes_explored