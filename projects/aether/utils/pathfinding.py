import heapq

def a_star(world, start, goal):
    """
    Finds the shortest path from start to goal on the WorldGrid using A*.
    Returns a list of (x, y) coordinates including the start and goal.
    Returns None if no path is found.
    """
    def heuristic(a, b):
        if len(a) == 3:
            return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        is_3d = len(current) == 3
        dirs = [(0,1,0), (0,-1,0), (1,0,0), (-1,0,0), (0,0,1), (0,0,-1)] if is_3d else [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for d in dirs:
            if is_3d:
                neighbor = (current[0] + d[0], current[1] + d[1], current[2] + d[2])
            else:
                neighbor = (current[0] + d[0], current[1] + d[1])

            # Check if neighbor is within bounds and not occupied
            in_bounds = (0 <= neighbor[0] < world.width and 0 <= neighbor[1] < world.height)
            if is_3d:
                in_bounds = in_bounds and (0 <= neighbor[2] < world.depth)

            if in_bounds:
                # Goal is always reachable even if occupied by another agent (we'll handle it)
                # But we should avoid obstacles.
                is_goal = neighbor == goal
                if world.get_item(neighbor) == 'obstacle' and not is_goal:
                    continue

                # In AETHER, agents also occupy cells. For pathfinding, we treat them as obstacles
                # unless it's the goal.
                if is_3d:
                    if neighbor in world.agents and not is_goal:
                        continue
                else:
                    if world.grid[neighbor[1]][neighbor[0]] is not None and not is_goal:
                        continue

                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))

    return None
