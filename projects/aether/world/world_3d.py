class World3D:
    """A 3D voxel grid environment for AETHER."""
    def __init__(self, size=(10, 10, 10)):
        self.width, self.height, self.depth = size
        # agents is a dict: (x,y,z) -> agent
        self.agents = {}
        # obstacles is a set: {(x,y,z), ...}
        self.obstacles = set()
        # items is a dict: (x,y,z) -> item_type
        self.items = {}

    def is_occupied(self, pos):
        x, y, z = pos
        if not (0 <= x < self.width and 0 <= y < self.height and 0 <= z < self.depth):
            return True
        return pos in self.agents or pos in self.obstacles

    def place_agent(self, agent, pos):
        if not self.is_occupied(pos):
            self.agents[pos] = agent
            return True
        return False

    def place_item(self, item_type, pos):
        if 0 <= pos[0] < self.width and 0 <= pos[1] < self.height and 0 <= pos[2] < self.depth:
            if item_type == 'obstacle':
                self.obstacles.add(pos)
            else:
                self.items[pos] = item_type
            return True
        return False

    def move_agent(self, agent, from_pos, to_pos):
        if not (0 <= to_pos[0] < self.width and 0 <= to_pos[1] < self.height and 0 <= to_pos[2] < self.depth):
            return False
        if from_pos in self.agents and self.agents[from_pos] == agent and not self.is_occupied(to_pos):
            del self.agents[from_pos]
            self.agents[to_pos] = agent
            return True
        return False

    def get_item(self, pos):
        return self.items.get(pos)
