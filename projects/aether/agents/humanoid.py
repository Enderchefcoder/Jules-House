import random
from utils.pathfinding import a_star

from core.brain import RobotBrain
import torch

class HumanoidAgent:
    """A humanoid robot agent for the AETHER simulation."""

    def __init__(self, name, world, position=(0, 0)):
        self.name = name
        self.world = world
        self.position = position
        self.battery = 100
        self.status = "Idle"
        self.is_3d = hasattr(world, 'depth')
        self.brain = RobotBrain(input_size=6 if self.is_3d else 4)

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
        if self.is_3d:
            # For 3D, iterate over items dict
            for pos, itype in self.world.items.items():
                if itype == 'charger':
                    dist = abs(self.position[0] - pos[0]) + abs(self.position[1] - pos[1]) + abs(self.position[2] - pos[2])
                    if dist < min_dist:
                        min_dist = dist
                        nearest = pos
        else:
            for y in range(self.world.height):
                for x in range(self.world.width):
                    if self.world.get_item((x, y)) == 'charger':
                        dist = abs(self.position[0] - x) + abs(self.position[1] - y)
                        if dist < min_dist:
                            min_dist = dist
                            nearest = (x, y)
        return nearest

    def get_state(self, target):
        if self.is_3d:
            return torch.tensor([float(self.position[0]), float(self.position[1]), float(self.position[2]),
                                float(target[0]), float(target[1]), float(target[2])])
        else:
            return torch.tensor([float(self.position[0]), float(self.position[1]),
                                float(target[0]), float(target[1])])

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
        target = self.find_nearest_charger()
        if self.battery < 30 and target:
            # Use Brain to "decide" intent (even if we still use A* for actual path)
            state = self.get_state(target)
            intent = self.brain.decide(state)

            if self.position == target:
                self.recharge()
                return

            path = a_star(self.world, self.position, target)
            if path and len(path) > 1:
                next_step = path[1]
                if self.is_3d:
                    dx = next_step[0] - self.position[0]
                    dy = next_step[1] - self.position[1]
                    dz = next_step[2] - self.position[2]
                    self.move_3d(dx, dy, dz)
                else:
                    dx = next_step[0] - self.position[0]
                    dy = next_step[1] - self.position[1]
                    self.move(dx, dy)
                self.status = f"Heading to charger at {target}"
                return

        # Random movement for simulation, avoiding obstacles
        moves = [(0,1,0), (0,-1,0), (1,0,0), (-1,0,0), (0,0,1), (0,0,-1), (0,0,0)] if self.is_3d else [(0,1), (0,-1), (1,0), (-1,0), (0,0)]
        random.shuffle(moves)
        for m in moves:
            if all(d == 0 for d in m):
                self.status = "Observing"
                break

            if self.is_3d:
                new_pos = (self.position[0] + m[0], self.position[1] + m[1], self.position[2] + m[2])
            else:
                new_pos = (self.position[0] + m[0], self.position[1] + m[1])

            if not self.world.is_occupied(new_pos):
                if self.is_3d:
                    if self.move_3d(*m): break
                else:
                    if self.move(*m): break
        else:
            self.status = "Stuck"

    def move_3d(self, dx, dy, dz):
        if self.battery < 5:
            return False
        new_pos = (self.position[0] + dx, self.position[1] + dy, self.position[2] + dz)
        if self.world.move_agent(self, self.position, new_pos):
            self.position = new_pos
            self.battery -= 5
            self.status = "Moving 3D"
            return True
        return False

    def __repr__(self):
        return f"HumanoidAgent({self.name}, {self.position}, {self.battery}%)"

if __name__ == "__main__":
    print("HumanoidAgent module loaded.")
