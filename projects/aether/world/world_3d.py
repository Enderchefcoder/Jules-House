class World3D:
    """A 3D voxel grid environment for AETHER."""
    def __init__(self, size=(10, 10, 10), use_atlas=False):
        self.width, self.height, self.depth = size
        # agents is a dict: (x,y,z) -> agent
        self.agents = {}
        # obstacles is a set: {(x,y,z), ...}
        self.obstacles = set()
        # items is a dict: (x,y,z) -> item_type
        self.items = {}

        if use_atlas:
            try:
                from projects.atlas.generator import TerrainGenerator
                gen = TerrainGenerator(size=size)
                self.obstacles = gen.get_world_obstacles()
                print(f"[World3D] Initialized with ATLAS Procedural Terrain ({len(self.obstacles)} voxels).")
            except ImportError:
                print("[World3D] ATLAS generator not found. Defaulting to empty world.")

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

    def remove_item(self, pos):
        """Removes an item (not an obstacle) from the specified position."""
        if pos in self.items:
            del self.items[pos]
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
        if pos in self.obstacles:
            return 'obstacle'
        return self.items.get(pos)
