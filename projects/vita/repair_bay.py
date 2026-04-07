class RepairBay:
    """
    A world item/facility where agents can go to perform repairs.
    Costs resources (Metal) and credits (NEXUS credits/balance).
    """
    def __init__(self, position):
        self.position = position
        self.repair_cost_metal = 5
        self.repair_cost_credits = 100.0

    def service_agent(self, agent):
        """Performs maintenance on an agent if they have the resources."""
        if not hasattr(agent, 'health_monitor'):
            return False

        if agent.inventory.get("Metal", 0) >= self.repair_cost_metal and agent.balance >= self.repair_cost_credits:
            agent.inventory["Metal"] -= self.repair_cost_metal
            agent.balance -= self.repair_cost_credits
            agent.health_monitor.perform_repair("Full")
            print(f"[VITA] {agent.name} fully repaired at RepairBay {self.position}.")
            return True
        else:
            print(f"[VITA] {agent.name} insufficient funds/metal for repair at {self.position}.")
            return False

if __name__ == "__main__":
    print("Project VITA: RepairBay module loaded.")
