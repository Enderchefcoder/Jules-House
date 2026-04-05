class EnergyGrid:
    """Manages the energy distribution and dynamic pricing for the simulation."""
    def __init__(self, base_price=1.0):
        self.base_price = base_price
        self.supply = 1000.0
        self.demand = 0.0
        self.current_price = base_price

    def update_price(self, solar_production):
        """Updates price based on supply (solar) and estimated demand."""
        self.supply += solar_production
        # Price increases with demand and decreases with supply
        # Simple formula: Price = Base * (Demand / (Supply + 1e-6))
        # For simplicity, we'll oscillate it
        self.current_price = self.base_price * (1.0 + (self.demand / (self.supply + 1)))
        print(f"[HELIOS Grid] Supply: {self.supply:.1f}, Demand: {self.demand:.1f}, Price: {self.current_price:.2f}")

    def consume(self, amount):
        if self.supply >= amount:
            self.supply -= amount
            self.demand += amount * 0.5 # Simplified demand tracking
            return True
        return False

if __name__ == "__main__":
    grid = EnergyGrid()
    grid.update_price(50.0)
    grid.consume(10.0)
    grid.update_price(20.0)
