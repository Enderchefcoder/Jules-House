import numpy as np

class TerrainGenerator:
    """
    Generates 3D voxel terrain for the AETHER ecosystem.
    Supports heightmaps (mountains/valleys) and volumetric caves.
    """
    def __init__(self, size=(20, 20, 20), seed=42):
        self.width, self.height, self.depth = size
        self.seed = seed
        np.random.seed(seed)

    def generate_heightmap(self, base_level=2, variance=5):
        """Generates a simple heightmap based on 2D noise (simulated)."""
        obstacles = set()
        for x in range(self.width):
            for y in range(self.height):
                # Simulated 2D noise for height
                h = base_level + int(variance * (np.sin(x / 3.0) * np.cos(y / 3.0) + 1))
                for z in range(min(h, self.depth)):
                    obstacles.add((x, y, z))
        return obstacles

    def generate_caves(self, density=0.05):
        """Generates volumetric cave pockets using 3D random distribution."""
        caves = set()
        num_caves = int(self.width * self.height * self.depth * density)
        for _ in range(num_caves):
            pos = (np.random.randint(0, self.width),
                   np.random.randint(0, self.height),
                   np.random.randint(0, self.depth))
            # Cave is a small 2x2x2 void (removing from obstacles later)
            for dx in range(2):
                for dy in range(2):
                    for dz in range(2):
                        vx, vy, vz = pos[0]+dx, pos[1]+dy, pos[2]+dz
                        if vx < self.width and vy < self.height and vz < self.depth:
                            caves.add((vx, vy, vz))
        return caves

    def get_world_obstacles(self):
        """Combines heightmap and caves to produce final obstacle set."""
        mountains = self.generate_heightmap()
        caves = self.generate_caves()
        # Voxel terrain: Mountains minus Caves
        return mountains - caves

if __name__ == "__main__":
    gen = TerrainGenerator()
    obs = gen.get_world_obstacles()
    print(f"Project ATLAS: Generated {len(obs)} voxel obstacles.")
