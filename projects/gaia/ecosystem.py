import random

class EcosystemManager:
    """Manages resource regeneration and biological hazards (simulated)."""
    def __init__(self, world):
        self.world = world
        self.regeneration_rate = 0.05 # 5% chance to spawn new resource per step

    def step(self):
        """Regenerates resources in empty voxels."""
        if random.random() < self.regeneration_rate:
            x = random.randint(0, self.world.width - 1)
            y = random.randint(0, self.world.height - 1)
            z = random.randint(0, self.world.depth - 1)
            pos = (x, y, z)

            if not self.world.is_occupied(pos) and self.world.get_item(pos) is None:
                res = random.choice(["Metal", "Data"])
                self.world.place_item(res, pos)
                # print(f"[GAIA] Ecosystem regenerated {res} at {pos}")

if __name__ == "__main__":
    print("Project GAIA: EcosystemManager loaded.")
