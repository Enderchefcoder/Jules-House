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
        self.build_materials = {"Metal": 20, "Alloy": 5} # Cost to build an outpost
        self.can_build = True

    def build_outpost(self):
        """Constructs a new charger/market hub or high-efficiency Beacon."""
        has_metal = self.inventory.get("Metal", 0) >= self.build_materials["Metal"]
        has_alloy = self.inventory.get("Alloy", 0) >= self.build_materials["Alloy"]

        if has_metal or has_alloy:
            if has_alloy:
                self.inventory["Alloy"] -= self.build_materials["Alloy"]
                print(f"[TITAN] {self.name} used refined ALLOY for construction.")
            else:
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
        """Dedicated method for research lab (costs more Data and Alloy)."""
        has_resources = (self.inventory.get("Metal", 0) >= 10 and self.inventory.get("Data", 0) >= 10) or \
                        (self.inventory.get("Alloy", 0) >= 10)

        if has_resources:
            if self.inventory.get("Alloy", 0) >= 10:
                self.inventory["Alloy"] -= 10
                print(f"[TITAN] {self.name} used 10 ALLOY for RESEARCH LAB.")
            else:
                self.inventory["Metal"] -= 10
                self.inventory["Data"] -= 10

            self.world.place_item("research_lab", self.position)
            print(f"[TITAN] {self.name} established a RESEARCH LAB at {self.position}!")
            return True
        return False

    def build_relay_station(self):
        """Dedicated method for relay station (costs more Metal/Alloy)."""
        has_resources = (self.inventory.get("Metal", 0) >= 20) or (self.inventory.get("Alloy", 0) >= 5)

        if has_resources:
            if self.inventory.get("Alloy", 0) >= 5:
                self.inventory["Alloy"] -= 5
                print(f"[TITAN] {self.name} used 5 ALLOY for RELAY STATION.")
            else:
                self.inventory["Metal"] -= 20

            self.world.place_item("relay_station", self.position)
            print(f"[TITAN] {self.name} deployed a RELAY STATION at {self.position}!")
            return True
        return False

    def perform_task(self):
        """Extended task performance: Titans prioritize building if they have materials."""
        # 2026 Autonomous Infrastructure Logic
        # Check swarm needs: If many agents are low health, prioritize Research Labs (which provide maintenance)
        # If communication is limited (simulated), build Relay Stations.

        has_alloy = self.inventory.get("Alloy", 0) >= 10
        has_metal = self.inventory.get("Metal", 0) >= 20

        if has_alloy or has_metal:
            # Simple swarm-need heuristics
            # 1. Check health of nearby agents (simulated)
            need_health = random.random() < 0.3 # 30% chance to prioritize lab
            if need_health and self.build_research_lab():
                return

            # 2. Check communication range (simulated)
            need_relay = random.random() < 0.2 # 20% chance to prioritize relay
            if need_relay and self.build_relay_station():
                return

            # 3. Default to general outpost if materials allow
            if self.inventory.get("Metal", 0) >= self.build_materials["Metal"] or \
               self.inventory.get("Alloy", 0) >= self.build_materials["Alloy"]:
                current_tile = self.world.get_item(self.position)
                if current_tile not in ["charger", "market_hub", "research_lab", "relay_station"]:
                    if self.build_outpost():
                        return

        # 4. Otherwise, behave like a standard agent (Scavenging)
        super().perform_task()

if __name__ == "__main__":
    print("HumanoidTitan module loaded.")
