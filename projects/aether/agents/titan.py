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

    def build_foundry_complex(self):
        """Constructs a new VULCAN foundry (costs Alloy and Metal)."""
        current_tile = self.world.get_item(self.position)
        if current_tile in ["charger", "market_hub", "research_lab", "relay_station", "foundry"]:
            return False

        has_resources = self.inventory.get("Alloy", 0) >= 10 and self.inventory.get("Metal", 0) >= 30
        if has_resources:
            self.inventory["Alloy"] -= 10
            self.inventory["Metal"] -= 30
            self.world.place_item("foundry", self.position)
            print(f"[TITAN] {self.name} established a FOUNDRY COMPLEX at {self.position}!")
            self.status = "Built Foundry"
            return True
        return False

    def scan_swarm_needs(self):
        """
        2026 Swarm-Aware Sensing: Titans assess environmental and agent states.
        Returns a tuple (need_health, need_relay, critical_agent) based on real simulation data.
        """
        need_health = False
        need_relay = False
        critical_agent = None

        # 1. Check health of nearby agents (Manhattan distance < 10)
        if hasattr(self.world, 'agents'):
            for a_pos, agent in self.world.agents.items():
                if agent.name != self.name:
                    dist = sum(abs(a - b) for a, b in zip(self.position, a_pos))
                    if dist < 10:
                        if hasattr(agent, 'health_monitor') and agent.health_monitor:
                            health = agent.health_monitor.get_overall_health()
                            if health < 50:
                                need_health = True
                                if health < 30:
                                    critical_agent = agent
                                    break # Found someone who needs immediate help

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

        return need_health, need_relay, critical_agent

    def cooperative_repair(self, target_agent):
        """
        HumanoidTitan Overload: Superior repair logic using Alloy.
        Costs 100 credits and 2 Alloy (or 5 Metal if no Alloy).
        """
        if target_agent == self:
            return False

        dist = sum(abs(a - b) for a, b in zip(self.position, target_agent.position))
        if dist > 1:
            return False

        if self.balance >= 100:
            if self.inventory.get("Alloy", 0) >= 2:
                if target_agent.health_monitor:
                    self.balance -= 100
                    self.inventory["Alloy"] -= 2
                    target_agent.health_monitor.perform_repair("Full")
                    print(f"[TITAN] SUPERIOR REPAIR performed on {target_agent.name} using ALLOY!")
                    return True
            elif self.inventory.get("Metal", 0) >= 5:
                # Fallback to standard repair
                return super().cooperative_repair(target_agent)
        return False

    def perform_task(self, agents=None):
        """Extended task performance: Titans prioritize building if they have materials."""
        # 2026 Autonomous Infrastructure Logic
        # Check swarm needs: If many agents are low health, prioritize Research Labs
        # If communication is limited, build Relay Stations.

        has_alloy = self.inventory.get("Alloy", 0) >= 10
        has_metal = self.inventory.get("Metal", 0) >= 20

        # 1. 2026 Swarm Mutual Aid: Check for critical agents first
        need_health, need_relay, critical_agent = self.scan_swarm_needs()

        if critical_agent:
            dist = sum(abs(a - b) for a, b in zip(self.position, critical_agent.position))
            if dist <= 1:
                if self.cooperative_repair(critical_agent):
                    self.status = f"Repaired {critical_agent.name}"
                    return
            else:
                # Move towards critical agent
                self.current_target = critical_agent.position
                # Proceed to movement logic below by skipping infrastructure checks for now

        if has_alloy or has_metal:
            # 2026: Informed Decision Making
            if need_health and self.build_research_lab():
                return

            if need_relay:
                if self.build_relay_station():
                    return
                else:
                    # Drive toward a location lacking coverage
                    # For simulation, we'll pick a random edge of the current known coverage
                    # or just a distant point if no relays exist
                    if not self.message_bus or not self.message_bus.relays:
                         self.current_target = (10, 10, 10)
                    else:
                         # Pick a position far from any relay
                         self.current_target = (random.randint(0, 19), random.randint(0, 19), random.randint(0, 19))

        # 2. Industrial Expansion: If resources are overflowing, build more Foundries
        if self.inventory.get("Alloy", 0) >= 20 and self.inventory.get("Metal", 0) >= 40:
             if self.build_foundry_complex():
                 return

        # 3. Default to general outpost if materials allow
        if self.inventory.get("Metal", 0) >= self.build_materials["Metal"] or \
           self.inventory.get("Alloy", 0) >= self.build_materials["Alloy"]:
            current_tile = self.world.get_item(self.position)
            if current_tile not in ["charger", "market_hub", "research_lab", "relay_station", "foundry"]:
                if self.build_outpost():
                    return

        # 4. Otherwise, behave like a standard agent (Scavenging)
        super().perform_task(agents=agents)

if __name__ == "__main__":
    print("HumanoidTitan module loaded.")
