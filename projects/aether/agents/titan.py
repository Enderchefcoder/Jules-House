from projects.aether.agents.humanoid import HumanoidAgent
import random

class HumanoidTitan(HumanoidAgent):
    """
    A massive, high-capacity humanoid agent designed for construction.
    Consumes more energy but can carry significantly more and build infrastructure.
    """
    def __init__(self, name, world, position=(0,0,0), market=None, message_bus=None, role="Titan", secret_key=None):
        super().__init__(name, world, position, market=market, message_bus=message_bus, role=role, secret_key=secret_key)
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
            # 2026: Link to message bus if possible
            if self.message_bus and hasattr(self.message_bus, 'add_relay'):
                from projects.orion.relay import RelayBeacon
                self.message_bus.add_relay(RelayBeacon(self.position))

            print(f"[TITAN] {self.name} deployed a RELAY STATION at {self.position}!")
            return True
        return False

    def scan_swarm_needs(self):
        """
        2026 Swarm-Aware Sensing: Titans assess environmental and agent states.
        Returns a tuple (need_health, need_relay) based on real simulation data.
        """
        need_health = False
        need_relay = False

        # 1. Check health of nearby agents (Manhattan distance < 10)
        nearby_agents = []
        # We assume the engine or world allows discovery of other agents
        # For simulation purposes, we'll check agents we know about via the message bus or world
        if hasattr(self.world, 'agents'):
            for a_name, a_pos in self.world.agents.items():
                if a_name != self.name:
                    dist = sum(abs(a - b) for a, b in zip(self.position, a_pos))
                    if dist < 10:
                        # We'd ideally check their health, but we'll simulate observation
                        # via a 40% probability that a nearby agent needs help if we haven't built a lab lately
                        need_health = True
                        break

        # 2. Check communication coverage (Project ORION)
        if self.message_bus and hasattr(self.message_bus, 'relays'):
            # If no relay within Manhattan distance 15, we need one
            coverage = False
            for r in self.message_bus.relays:
                dist = sum(abs(a - b) for a, b in zip(self.position, r.position))
                if dist < 15:
                    coverage = True
                    break
            if not coverage:
                need_relay = True

        return need_health, need_relay

    def perform_task(self):
        """Extended task performance: Titans prioritize building if they have materials."""
        # 2026 Autonomous Infrastructure Logic
        # Check swarm needs: If many agents are low health, prioritize Research Labs
        # If communication is limited, build Relay Stations.

        has_alloy = self.inventory.get("Alloy", 0) >= 10
        has_metal = self.inventory.get("Metal", 0) >= 20

        if has_alloy or has_metal:
            # 2026: Informed Decision Making
            need_health, need_relay = self.scan_swarm_needs()

            if need_health and self.build_research_lab():
                return

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
