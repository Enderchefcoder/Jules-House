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
        """Constructs a new charger/market hub if enough materials are present."""
        if self.inventory.get("Metal", 0) >= self.build_materials["Metal"]:
            self.inventory["Metal"] -= self.build_materials["Metal"]
            # Decide what to build
            choice = random.choice(["charger", "market_hub"])
            self.world.place_item(choice, self.position)
            print(f"[TITAN] {self.name} constructed a {choice} at {self.position}!")
            self.status = f"Built {choice}"
            return True
        else:
            self.status = "Insufficient Materials for Outpost"
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
