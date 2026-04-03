class WorldGrid:
    """A 2D grid representing the AETHER environment."""

    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        # grid stores the agent object or None
        self.grid = [[None for _ in range(width)] for _ in range(height)]

    def is_occupied(self, position):
        """Checks if a cell is occupied by an agent."""
        x, y = position
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x] is not None
        return True # Out of bounds is treated as occupied

    def place_agent(self, agent, position):
        """Places an agent at a given position on the grid."""
        x, y = position
        if not self.is_occupied(position):
            self.grid[y][x] = agent
            return True
        return False

    def move_agent(self, agent, from_pos, to_pos):
        """Moves an agent from one position to another."""
        fx, fy = from_pos
        tx, ty = to_pos

        if not (0 <= tx < self.width and 0 <= ty < self.height):
             return False # Cannot move out of bounds

        if self.grid[fy][fx] == agent and not self.is_occupied(to_pos):
            self.grid[fy][fx] = None
            self.grid[ty][tx] = agent
            return True
        return False

    def get_status(self):
        """Returns a string representation of the grid (simple for now)."""
        status_lines = []
        for row in self.grid:
            line = "".join(["R" if cell else "." for cell in row])
            status_lines.append(line)
        return "\n".join(status_lines)

if __name__ == "__main__":
    world = WorldGrid()
    print(world.get_status())
