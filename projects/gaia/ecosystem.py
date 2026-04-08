import random

class EcosystemManager:
    """Manages resource regeneration and biological hazards (simulated)."""
    def __init__(self, world):
        self.world = world
        self.regeneration_rate = 0.05 # 5% chance to spawn new resource per step

    def step(self):
        """Regenerates resources in empty voxels using cluster logic."""
        if random.random() < self.regeneration_rate:
            # 1. Select a seed location
            x = random.randint(0, self.world.width - 1)
            y = random.randint(0, self.world.height - 1)
            z = random.randint(0, self.world.depth - 1)

            res_type = random.choice(["Metal", "Data"])
            cluster_size = random.randint(2, 5)

            # 2. Grow a cluster
            for _ in range(cluster_size):
                dx, dy, dz = random.randint(-1, 1), random.randint(-1, 1), random.randint(-1, 1)
                pos = (x + dx, y + dy, z + dz)

                # Check bounds and occupancy
                if 0 <= pos[0] < self.world.width and 0 <= pos[1] < self.world.height and 0 <= pos[2] < self.world.depth:
                    if not self.world.is_occupied(pos) and self.world.get_item(pos) is None:
                        self.world.place_item(res_type, pos)
                        # print(f"[GAIA] Ecosystem grew {res_type} cluster element at {pos}")

if __name__ == "__main__":
    print("Project GAIA: EcosystemManager loaded.")
