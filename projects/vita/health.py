import random

class HealthMonitor:
    """
    Simulates physical hardware degradation in humanoid agents.
    Tracks 'Joint Wear', 'Circuit Integrity', and 'Optical Clarity'.
    """
    def __init__(self, agent_name):
        self.agent_name = agent_name
        self.joint_wear = 0.0      # 0 to 100 (100 is failure)
        self.circuit_degradation = 0.0
        self.optical_clarity = 100.0 # 100 to 0 (0 is failure)
        self.maintenance_required = False

    def step(self, movement_type="Standard"):
        """Degrades health based on activity."""
        wear_rate = 0.05
        if movement_type == "Heavy": # Titans or fast moves
            wear_rate = 0.15

        self.joint_wear += random.uniform(0, wear_rate)
        self.circuit_degradation += random.uniform(0, 0.02)

        # 1% chance for optical smudging each step
        if random.random() < 0.01:
            self.optical_clarity -= random.uniform(1, 5)

        if self.joint_wear > 70 or self.circuit_degradation > 60:
            self.maintenance_required = True

    def get_overall_health(self):
        """Returns health as a percentage."""
        avg_degradation = (self.joint_wear + self.circuit_degradation + (100 - self.optical_clarity)) / 3.0
        return max(0, 100 - avg_degradation)

    def perform_repair(self, repair_type="Full"):
        """Restores health metrics."""
        if repair_type == "Full":
            self.joint_wear = 0.0
            self.circuit_degradation = 0.0
            self.optical_clarity = 100.0
            self.maintenance_required = False
        elif repair_type == "QuickFix":
            self.joint_wear = max(0, self.joint_wear - 30)
            self.circuit_degradation = max(0, self.circuit_degradation - 20)

    def __repr__(self):
        return f"Health({self.get_overall_health():.1f}%, Maintenance: {self.maintenance_required})"

if __name__ == "__main__":
    print("Project VITA: HealthMonitor module loaded.")
