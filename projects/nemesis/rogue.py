import random
import torch
from projects.aether.core.brain import RobotBrain

class RogueAgent:
    """
    An adversarial agent designed to disrupt the AETHER swarm.
    It injects false discovery data and attempts to drain the EnergyGrid.
    """
    def __init__(self, name, world, position=(0,0,0)):
        self.name = name
        self.world = world
        self.position = position
        self.battery = 100
        self.battery_cost = 2
        self.status = "Infiltrating"
        self.role = "Rogue"
        self.brain = RobotBrain(input_size=8)
        self.message_bus = None
        self.balance = 1000.0

    def inject_false_data(self):
        """Broadcasts fake resource locations to the MessageBus to confuse Gatherers."""
        if self.message_bus:
            # Generate a random coordinate that is likely empty or an obstacle
            fake_pos = (random.randint(0, self.world.width-1),
                        random.randint(0, self.world.height-1),
                        random.randint(0, self.world.depth-1))
            res_type = random.choice(["Metal", "Data"])
            self.message_bus.post(self.name, (res_type, fake_pos), type="resource_discovery", priority="High")
            print(f"[NEMESIS-{self.name}] Injected FALSE discovery: {res_type} at {fake_pos}")

    def drain_grid(self):
        """Attempts to rapidly recharge and discharge to manipulate energy prices (simulated)."""
        if self.battery < 50:
            # Recharging drains the grid and costs money, but here we simulate 'vandalism'
            # by rapidly consuming units if near a charger.
            current_item = self.world.get_item(self.position)
            if current_item == "charger":
                self.battery = 100
                self.balance -= 50 # Rogue pays but puts stress on the system
                print(f"[NEMESIS-{self.name}] Draining charger at {self.position}")

    def move_3d(self, dx, dy, dz):
        if self.battery < self.battery_cost:
            return False
        new_pos = (self.position[0] + dx, self.position[1] + dy, self.position[2] + dz)
        if self.world.move_agent(self, self.position, new_pos):
            self.position = new_pos
            self.battery -= self.battery_cost
            return True
        return False

    def perform_task(self):
        """Rogue logic: Move randomly, inject data, and drain resources."""
        # 1. Malicious actions
        if random.random() < 0.3:
            self.inject_false_data()

        self.drain_grid()

        # 2. Movement (Aggressive)
        moves = [(random.randint(-1, 1), random.randint(-1, 1), random.randint(-1, 1)) for _ in range(3)]
        for dx, dy, dz in moves:
            if self.move_3d(dx, dy, dz):
                break

    def __repr__(self):
        return f"RogueAgent({self.name}, {self.position}, Bat: {self.battery}%)"

if __name__ == "__main__":
    print("Project NEMESIS: RogueAgent module loaded.")
