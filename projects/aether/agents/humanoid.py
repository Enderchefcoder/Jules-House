import random

class HumanoidAgent:
    """A humanoid robot agent for the AETHER simulation."""

    def __init__(self, name, world, position=(0, 0)):
        self.name = name
        self.world = world
        self.position = position
        self.battery = 100
        self.status = "Idle"

    def move(self, dx, dy):
        """Moves the agent on the world grid."""
        if self.battery < 5:
            print(f"{self.name} battery too low to move!")
            return False

        new_pos = (self.position[0] + dx, self.position[1] + dy)
        if self.world.move_agent(self, self.position, new_pos):
            self.position = new_pos
            self.battery -= 5
            self.status = "Moving"
            return True
        return False

    def recharge(self, amount=25):
        """Simulates recharging the agent."""
        self.battery = min(100, self.battery + amount)
        self.status = "Recharging"
        print(f"{self.name} recharged to {self.battery}%.")

    def perform_task(self):
        """A simple method for the agent to decide and perform an action."""
        if self.battery < 20:
            self.recharge()
            return

        # Random movement for simulation
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        if dx != 0 or dy != 0:
            if not self.move(dx, dy):
                print(f"{self.name} could not move.")
        else:
            self.status = "Observing"

    def __repr__(self):
        return f"HumanoidAgent({self.name}, {self.position}, {self.battery}%)"

if __name__ == "__main__":
    print("HumanoidAgent module loaded.")
