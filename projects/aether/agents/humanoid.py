import random
from utils.pathfinding import a_star
from core.brain import RobotBrain
import torch

# Try to import market from chronos
try:
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
    from chronos.market import Market
except ImportError:
    Market = None

class HumanoidAgent:
    """A humanoid robot agent for the AETHER simulation with economic and swarm capabilities."""

    def __init__(self, name, world, position=(0, 0), market=None, message_bus=None):
        self.name = name
        self.world = world
        self.position = position
        self.battery = 100
        self.status = "Idle"
        self.is_3d = hasattr(world, 'depth')
        self.brain = RobotBrain(input_size=6 if self.is_3d else 4)

        # Economic attributes
        self.inventory = {"Metal": 0, "Data": 0}
        self.balance = 500.0  # Starting capital
        self.market = market
        self.message_bus = message_bus
        self.shared_resource_locations = {} # {resource_type: [pos1, pos2]}

    def move(self, dx, dy):
        """Moves the agent on the world grid."""
        if self.battery < 5:
            print(f"{self.name} battery too low to move!")
            return False

        new_pos = (self.position[0] + dx, self.position[1] + dy)
        # Handle 3D coordinates if necessary
        if self.is_3d and len(new_pos) == 2:
            new_pos = (new_pos[0], new_pos[1], self.position[2])

        if self.world.move_agent(self, self.position, new_pos):
            self.position = new_pos
            self.battery -= 5
            self.status = "Moving"
            return True
        return False

    def move_3d(self, dx, dy, dz):
        """Moves the agent in 3D space."""
        if self.battery < 5:
            print(f"{self.name} battery too low to move!")
            return False
        new_pos = (self.position[0] + dx, self.position[1] + dy, self.position[2] + dz)
        if self.world.move_agent(self, self.position, new_pos):
            self.position = new_pos
            self.battery -= 5
            self.status = "Moving 3D"
            return True
        return False

    def recharge(self, amount=25):
        """Simulates recharging the agent. Costs money if a market is present."""
        if self.market:
            price_per_unit = self.market.get_price("Energy") / 10.0 # Scaling price
            cost = amount * price_per_unit
            if self.balance >= cost:
                self.balance -= cost
                self.battery = min(100, self.battery + amount)
                self.status = f"Recharging (Cost: {cost:.2f})"
                print(f"{self.name} recharged to {self.battery}%. Balance: {self.balance:.2f}")
                return True
            else:
                self.status = "Insolvent - Cannot Recharge"
                print(f"{self.name} cannot afford recharge!")
                return False
        else:
            self.battery = min(100, self.battery + amount)
            self.status = "Recharging"
            return True

    def find_nearest_item(self, item_types):
        """Scans the world for the nearest item of certain types."""
        if isinstance(item_types, str):
            item_types = [item_types]

        min_dist = float('inf')
        nearest = None

        # Access world items
        if self.is_3d:
            items_to_check = self.world.items.items()
        else:
            # For 2D WorldGrid, we need to iterate (less efficient but works for small grids)
            items_to_check = []
            for y in range(self.world.height):
                for x in range(self.world.width):
                    it = self.world.get_item((x, y))
                    if it:
                        items_to_check.append(((x, y), it))

        for pos, itype in items_to_check:
            if itype in item_types:
                dist = sum(abs(a - b) for a, b in zip(self.position, pos))
                if dist < min_dist:
                    min_dist = dist
                    nearest = pos
        return nearest

    def get_state(self, target):
        if self.is_3d:
            return torch.tensor([float(self.position[0]), float(self.position[1]), float(self.position[2]),
                                float(target[0]), float(target[1]), float(target[2])])
        else:
            return torch.tensor([float(self.position[0]), float(self.position[1]),
                                float(target[0]), float(target[1])])

    def process_messages(self):
        """Checks the message bus for updates from other agents."""
        if not self.message_bus:
            return

        messages = self.message_bus.get_messages(type="resource_discovery")
        for m in messages:
            if m["sender"] != self.name:
                res_type, pos = m["content"]
                if res_type not in self.shared_resource_locations:
                    self.shared_resource_locations[res_type] = []
                if pos not in self.shared_resource_locations[res_type]:
                    self.shared_resource_locations[res_type].append(pos)
                    print(f"{self.name} received broadcast: {res_type} at {pos}")

    def perform_task(self):
        """Decides and performs an action based on state, battery, and economy."""
        # 0. Process swarm communication
        self.process_messages()

        # 1. Check current tile for collection or interaction
        current_item = self.world.get_item(self.position)

        if current_item in ["Metal", "Data"]:
            self.inventory[current_item] += 1
            if hasattr(self.world, 'remove_item'):
                self.world.remove_item(self.position)

            # Swarm intelligence: Broadcast discovery
            if self.message_bus:
                self.message_bus.post(self.name, (current_item, self.position), type="resource_discovery")
                print(f"{self.name} broadcasting discovery: {current_item} at {self.position}")

            print(f"{self.name} collected {current_item}. Inventory: {self.inventory}")
            self.status = f"Collected {current_item}"
            return

        if current_item == "market_hub":
            if self.market:
                total_sale = 0
                for res, amt in self.inventory.items():
                    if amt > 0:
                        price = self.market.get_price(res)
                        total_sale += price * amt
                        self.inventory[res] = 0
                if total_sale > 0:
                    self.balance += total_sale
                    print(f"{self.name} sold inventory for {total_sale:.2f}. Balance: {self.balance:.2f}")
                    self.status = f"Sold Goods (+{total_sale:.2f})"
                    return

        if current_item == "charger" and self.battery < 90:
            if self.recharge():
                return

        # 2. Decide Target
        target = None
        if self.battery < 30:
            target = self.find_nearest_item("charger")

        if not target and (self.inventory["Metal"] > 0 or self.inventory["Data"] > 0):
            target = self.find_nearest_item("market_hub")

        if not target:
            # Check shared memory first
            for res in ["Metal", "Data"]:
                if res in self.shared_resource_locations and self.shared_resource_locations[res]:
                    # Verify if item still exists at known location
                    candidate = self.shared_resource_locations[res][0]
                    if self.world.get_item(candidate) == res:
                        target = candidate
                        break
                    else:
                        # Stale information
                        self.shared_resource_locations[res].pop(0)

            if not target:
                target = self.find_nearest_item(["Metal", "Data"])

        # 3. Move towards target
        if target:
            if self.position == target:
                # Already there, status update
                self.status = f"At {self.world.get_item(target)}"
                return

            path = a_star(self.world, self.position, target)
            if path and len(path) > 1:
                next_step = path[1]
                dx = next_step[0] - self.position[0]
                dy = next_step[1] - self.position[1]
                if self.is_3d:
                    dz = next_step[2] - self.position[2]
                    self.move_3d(dx, dy, dz)
                else:
                    self.move(dx, dy)
                self.status = f"Heading to {target}"
                return

        # 4. Fallback: Random movement
        moves = [(0,1,0), (0,-1,0), (1,0,0), (-1,0,0), (0,0,1), (0,0,-1)] if self.is_3d else [(0,1), (0,-1), (1,0), (-1,0)]
        random.shuffle(moves)
        for m in moves:
            if self.is_3d:
                if self.move_3d(*m): return
            else:
                if self.move(*m): return

        self.status = "Idling"

    def __repr__(self):
        return f"HumanoidAgent({self.name}, {self.position}, Bat: {self.battery}%, Bal: {self.balance:.2f})"

if __name__ == "__main__":
    print("HumanoidAgent module loaded.")
