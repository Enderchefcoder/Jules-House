import random

class HazardManager:
    """Manages dynamic environmental hazards in the AETHER world."""

    def __init__(self, world):
        self.world = world
        self.hazards = {} # {(x,y,z): type}
        self.is_3d = hasattr(world, 'depth')

    def spawn_hazard(self):
        """Randomly places a hazard in the world."""
        if self.is_3d:
            size = (self.world.width, self.world.height, self.world.depth)
            pos = tuple(random.randint(0, s - 1) for s in size)
        else:
            size = (self.world.width, self.world.height)
            pos = tuple(random.randint(0, s - 1) for s in size)

        # Don't overwrite existing items or agents
        if self.world.get_item(pos) is None and pos not in getattr(self.world, 'agents', {}):
            hazard_type = random.choice(["Radiation", "Static", "Void"])
            self.hazards[pos] = hazard_type
            print(f"[HAZARD] {hazard_type} spawned at {pos}")
            return True
        return False

    def step(self, agents):
        """Updates hazards and applies effects to agents."""
        # 10% chance to spawn a new hazard each step
        if random.random() < 0.1:
            self.spawn_hazard()

        # Apply effects
        for agent in agents:
            if agent.position in self.hazards:
                h_type = self.hazards[agent.position]
                if h_type == "Radiation":
                    agent.battery -= 10
                    print(f"[ALARM] {agent.name} hit by Radiation! Battery drained.")
                elif h_type == "Static":
                    agent.status = "Glitching"
                    print(f"[ALARM] {agent.name} hit by Static! System glitching.")
                elif h_type == "Void":
                    agent.balance -= 5.0
                    print(f"[ALARM] {agent.name} hit by Void! NEXUS Credits lost.")

        # Hazards dissipate over time
        if random.random() < 0.2 and self.hazards:
            pos = random.choice(list(self.hazards.keys()))
            del self.hazards[pos]
            print(f"[HAZARD] Hazard at {pos} dissipated.")

    def get_hazard(self, pos):
        return self.hazards.get(pos)
