from projects.aether.agents.humanoid import HumanoidAgent
import random

class HumanoidTitan(HumanoidAgent):
    """
    A massive, high-capacity humanoid agent designed for construction.
    Consumes more energy but can carry significantly more and build infrastructure.
    """
    def __init__(self, name, world, position=(0,0,0), role="Titan"):
        super().__init__(name, world, position, role=role)
        self.battery_cost = 15 # Higher consumption
        self.inventory_capacity = 50 # Massive capacity
        self.build_materials = {"Metal": 20} # Cost to build an outpost
        self.can_build = True

    def build_outpost(self):
        """Constructs a new charger/market hub or high-efficiency Beacon."""
        if self.inventory.get("Metal", 0) >= self.build_materials["Metal"]:
            self.inventory["Metal"] -= self.build_materials["Metal"]
            # Decide what to build
            choice = random.choice(["charger", "market_hub", "outpost_beacon", "research_lab", "relay_station"])
            self.world.place_item(choice, self.position)

            print(f"[TITAN] {self.name} constructed a {choice.upper()} at {self.position}!")
            self.status = f"Built {choice}"
            return True
        else:
            self.status = "Insufficient Materials for Outpost"
            return False

    def build_research_lab(self):
        """Dedicated method for research lab (costs more Data)."""
        if self.inventory.get("Metal", 0) >= 10 and self.inventory.get("Data", 0) >= 10:
            self.inventory["Metal"] -= 10
            self.inventory["Data"] -= 10
            self.world.place_item("research_lab", self.position)
            print(f"[TITAN] {self.name} established a RESEARCH LAB at {self.position}!")
            return True
        return False

    def build_relay_station(self):
        """Dedicated method for relay station (costs more Metal)."""
        if self.inventory.get("Metal", 0) >= 20:
            self.inventory["Metal"] -= 20
            self.world.place_item("relay_station", self.position)
            print(f"[TITAN] {self.name} deployed a RELAY STATION at {self.position}!")
            return True
        return False

    def perform_task(self):
        """Extended task performance: Titans prioritize building if they have metal."""
        # 1. If we have enough metal, try to build an outpost in a new area
        if self.inventory.get("Metal", 0) >= self.build_materials["Metal"]:
            # Simple heuristic: don't build on top of existing chargers/markets
            current_tile = self.world.get_item(self.position)
            if current_tile not in ["charger", "market_hub"]:
                if self.build_outpost():
                    return

        # 2. Otherwise, behave like a standard agent (Scavenging Metal)
        super().perform_task()

if __name__ == "__main__":
    print("HumanoidTitan module loaded.")
