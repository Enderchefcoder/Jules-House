class Robot:
    """A simple robot class to simulate basic factory operations and state management."""

    def __init__(self, name, battery_level=100, position=(0, 0)):
        self.name = name
        self.battery_level = battery_level
        self.position = position  # (x, y)
        self.is_recharging = False

    def move(self, dx, dy):
        """Moves the robot by the specified displacement (dx, dy)."""
        if self.battery_level <= 0:
            print(f"Error: {self.name} has no battery and cannot move!")
            return False

        if self.is_recharging:
            print(f"Error: {self.name} is currently recharging and cannot move!")
            return False

        # Calculate energy cost: 1% battery per unit moved
        distance = (dx**2 + dy**2)**0.5
        energy_cost = int(distance) + 1  # Minimum cost of 1%

        if self.battery_level < energy_cost:
            print(f"Error: Not enough battery for {self.name} to complete the move.")
            return False

        self.battery_level -= energy_cost
        self.position = (self.position[0] + dx, self.position[1] + dy)
        print(f"{self.name} moved to {self.position}. Battery: {self.battery_level}%")
        return True

    def recharge(self, amount=20):
        """Simulates recharging the robot's battery."""
        self.is_recharging = True
        self.battery_level = min(100, self.battery_level + amount)
        print(f"{self.name} is recharging... Battery: {self.battery_level}%")
        self.is_recharging = False
        return True

    def report_status(self):
        """Returns a string describing the robot's current status."""
        return f"Robot: {self.name} | Position: {self.position} | Battery: {self.battery_level}%"

if __name__ == "__main__":
    # Quick sanity check
    bot = Robot("TestBot")
    print(bot.report_status())
    bot.move(3, 4)
    print(bot.report_status())
    bot.recharge(10)
    print(bot.report_status())
