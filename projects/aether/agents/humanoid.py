import random
from utils.pathfinding import a_star

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

    def find_nearest_charger(self):
        """Scans the world for the nearest charger."""
        min_dist = float('inf')
        nearest = None
        for y in range(self.world.height):
            for x in range(self.world.width):
                if self.world.get_item((x, y)) == 'charger':
                    dist = abs(self.position[0] - x) + abs(self.position[1] - y)
                    if dist < min_dist:
                        min_dist = dist
                        nearest = (x, y)
        return nearest

    def perform_task(self):
        """Decides and performs an action based on state and battery."""
        if self.battery < 10:
             # Critical battery, try to recharge if on charger, else stay still
             if self.world.get_item(self.position) == 'charger':
                 self.recharge()
             else:
                 self.status = "Low Power Mode"
             return

        # If battery is low, find and move to charger
        if self.battery < 30:
            target = self.find_nearest_charger()
            if target:
                if self.position == target:
                    self.recharge()
                    return

                path = a_star(self.world, self.position, target)
                if path and len(path) > 1:
                    next_step = path[1]
                    dx = next_step[0] - self.position[0]
                    dy = next_step[1] - self.position[1]
                    self.move(dx, dy)
                    self.status = f"Heading to charger at {target}"
                    return

        # Random movement for simulation, avoiding obstacles
        moves = [(0,1), (0,-1), (1,0), (-1,0), (0,0)]
        random.shuffle(moves)
        for dx, dy in moves:
            if dx == 0 and dy == 0:
                self.status = "Observing"
                break

            new_pos = (self.position[0] + dx, self.position[1] + dy)
            if not self.world.is_occupied(new_pos):
                if self.move(dx, dy):
                    break
        else:
            self.status = "Stuck"

    def __repr__(self):
        return f"HumanoidAgent({self.name}, {self.position}, {self.battery}%)"

if __name__ == "__main__":
    print("HumanoidAgent module loaded.")
