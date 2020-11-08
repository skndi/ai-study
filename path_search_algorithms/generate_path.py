import collections
def reconstruct_path(came_from, current):
    total_path = collections.deque();
    total_path.append(current);

    while current in came_from:
        current = came_from[current];
        total_path.appendleft(current);

    return total_path;
