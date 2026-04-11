import random
import torch
from projects.aether.core.brain import RobotBrain

class DroneAgent:
    """
    A high-speed, low-capacity mapping drone for the AETHER ecosystem.
    Focuses on 'unfogging' the environment for ground units.
    """
    def __init__(self, name, world, position=(0,0,0)):
        self.name = name
        self.world = world
        self.position = position
        self.battery = 100
        self.battery_cost = 1 # Very efficient movement
        self.status = "Idling"
        self.role = "Drone"
        # Drones use a simpler input for now or match 3D brain size
        self.brain = RobotBrain(input_size=10) # Match 3D brain size
        self.view_distance = 5 # Can see 5 units in all directions
        self.message_bus = None
        self.mapped_area = set()

    def scan_environment(self):
        """Scans nearby voxels and broadcasts found resources to the swarm."""
        discovered = []
        x0, y0, z0 = self.position
        for x in range(x0 - self.view_distance, x0 + self.view_distance + 1):
            for y in range(y0 - self.view_distance, y0 + self.view_distance + 1):
                for z in range(z0 - self.view_distance, z0 + self.view_distance + 1):
                    pos = (x, y, z)
                    if pos not in self.mapped_area:
                        self.mapped_area.add(pos)
                        item = self.world.get_item(pos)
                        if item in ["Metal", "Data"]:
                            discovered.append((item, pos))

        if discovered and self.message_bus:
            for item, pos in discovered:
                # Drones post directly to collective memory via resource_discovery type
                self.message_bus.post(self.name, (item, pos), type="resource_discovery")
            print(f"[{self.name}] Mapped area and discovered {len(discovered)} resources!")

    def move_3d(self, dx, dy, dz):
        """High-speed movement in 3D space."""
        if self.battery < self.battery_cost:
            return False

        new_pos = (self.position[0] + dx, self.position[1] + dy, self.position[2] + dz)

        # ZEPHYR-SPECIFIC 3D Pathfinding: Drones fly over ground-level obstacles.
        # They only collide if the obstacle height matches the drone altitude.
        if 0 <= new_pos[0] < self.world.width and 0 <= new_pos[1] < self.world.height and 0 <= new_pos[2] < self.world.depth:
            item = self.world.get_item(new_pos)
            # Fly over anything unless it's a solid obstacle at the same altitude
            if item == 'obstacle':
                # Simplified collision: only collide if we are in the bottom 25% of the world height (mountains)
                if new_pos[2] < self.world.depth // 4:
                    print(f"[{self.name}] Terrain collision avoided at {new_pos}.")
                    return False

            self.position = new_pos
            self.battery -= self.battery_cost
            self.status = "Scouting"
            return True
        return False

    def navigate_to_altitude(self, target_z):
        """Adjusts altitude to avoid terrain or turbulence."""
        dz = 1 if target_z > self.position[2] else -1 if target_z < self.position[2] else 0
        if dz != 0:
            self.move_3d(0, 0, dz)

    def perform_task(self):
        """Mapping logic: move randomly or towards unmapped sectors."""
        # 1. Scan current location
        self.scan_environment()

        # 2. Battery management
        if self.battery < 10:
            # Fly to nearest charger
            nearest_charger = self.find_nearest_item("charger")
            if nearest_charger:
                self.move_towards(nearest_charger)
                return

        # 3. Random scouting movement (Drones move 2 steps at a time)
        moves = [(random.randint(-2, 2), random.randint(-2, 2), random.randint(-2, 2)) for _ in range(3)]
        for dx, dy, dz in moves:
            if self.move_3d(dx, dy, dz):
                break

    def find_nearest_item(self, item_type):
        min_dist = float('inf')
        nearest = None
        for pos, itype in self.world.items.items():
            if itype == item_type:
                dist = sum(abs(a - b) for a, b in zip(self.position, pos))
                if dist < min_dist:
                    min_dist = dist
                    nearest = pos
        return nearest

    def move_towards(self, target):
        dx = 1 if target[0] > self.position[0] else -1 if target[0] < self.position[0] else 0
        dy = 1 if target[1] > self.position[1] else -1 if target[1] < self.position[1] else 0
        dz = 1 if target[2] > self.position[2] else -1 if target[2] < self.position[2] else 0
        self.move_3d(dx, dy, dz)

    def __repr__(self):
        return f"DroneAgent({self.name}, {self.position}, Bat: {self.battery}%)"

if __name__ == "__main__":
    print("Project ZEPHYR: DroneAgent module loaded.")
