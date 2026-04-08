class Foundry:
    """
    Project VULCAN: Advanced Manufacturing Foundry.
    Refines raw Metal and Energy into high-grade Alloy.
    """
    def __init__(self, position):
        self.position = position
        self.metal_input = 0
        self.energy_input = 0
        self.alloy_output = 0
        self.conversion_rate = 5 # 5 Metal + 5 Energy -> 1 Alloy

    def deposit_resources(self, metal=0, energy=0):
        self.metal_input += metal
        self.energy_input += energy
        print(f"[VULCAN] Foundry at {self.position} received resources: Metal={metal}, Energy={energy}")

    def process(self):
        """Processes available resources into Alloy."""
        can_produce = min(self.metal_input // self.conversion_rate, self.energy_input // self.conversion_rate)
        if can_produce > 0:
            self.metal_input -= can_produce * self.conversion_rate
            self.energy_input -= can_produce * self.conversion_rate
            self.alloy_output += can_produce
            print(f"[VULCAN] Foundry at {self.position} produced {can_produce} Alloy!")
            return can_produce
        return 0

    def collect_alloy(self):
        amount = self.alloy_output
        self.alloy_output = 0
        return amount

    def __repr__(self):
        return f"Foundry({self.position}, Metal: {self.metal_input}, Energy: {self.energy_input}, Alloy: {self.alloy_output})"
