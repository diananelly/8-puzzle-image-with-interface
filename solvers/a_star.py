import heapq
from utils.puzzle_utils_1 import find_blank, swap, get_neighbors

def manhattan_distance(state, goal_state):
    distance = 0
    for i in range(9):
        if state[i] != 0:
            goal_pos = goal_state.index(state[i])
            goal_row, goal_col = divmod(goal_pos, 3)
            current_row, current_col = divmod(i, 3)
            distance += abs(goal_row - current_row) + abs(goal_col - current_col)
    return distance

def a_star(initial_state, goal_state):
    pq = []
    heapq.heappush(pq, (manhattan_distance(initial_state, goal_state), 0, initial_state))
    g_map = {initial_state: 0}
    parent_map = {initial_state: None}
    visited = set()
    nodes_explored = 0

    while pq:
        _, current_cost, current_state = heapq.heappop(pq)
        nodes_explored += 1

        if current_state == goal_state:
            path = []
            while current_state:
                path.append(current_state)
                current_state = parent_map[current_state]
            return path[::-1], nodes_explored

        visited.add(current_state)

        for neighbor in get_neighbors(current_state):
            if neighbor not in visited:
                new_cost = current_cost + 1
                h_value = manhattan_distance(neighbor, goal_state)
                f_value = new_cost + h_value
                if neighbor not in g_map or new_cost < g_map[neighbor]:
                    g_map[neighbor] = new_cost
                    parent_map[neighbor] = current_state
                    heapq.heappush(pq, (f_value, new_cost, neighbor))

    return None, nodes_explored