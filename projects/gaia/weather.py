import random

class WeatherSystem:
    """
    Manages dynamic environmental states for the AETHER ecosystem.
    Affects energy production, agent movement, and health.
    """
    def __init__(self):
        self.weather_types = {
            "Clear": {"energy": 1.0, "health_impact": 0, "comms_disruption": 0},
            "Heatwave": {"energy": 1.5, "health_impact": -1, "comms_disruption": 0.1},
            "Storm": {"energy": 0.3, "health_impact": 0, "comms_disruption": 0.4},
            "Acid Rain": {"energy": 0.5, "health_impact": -5, "comms_disruption": 0.2},
            "Solar Flare": {"energy": 2.0, "health_impact": -2, "comms_disruption": 0.9}
        }
        self.current_weather = "Clear"

    def step(self):
        """Randomly transitions weather states."""
        if random.random() < 0.2: # 20% chance of weather change
            self.current_weather = random.choice(list(self.weather_types.keys()))
            print(f"[GAIA] Weather shifted to: {self.current_weather}")

    def get_modifiers(self):
        return self.weather_types.get(self.current_weather, self.weather_types["Clear"])

    def apply_effects(self, agents):
        """Applies direct environmental effects to agents (e.g., health decay)."""
        mods = self.get_modifiers()
        impact = mods["health_impact"]
        if impact != 0:
            for agent in agents:
                if hasattr(agent, 'health_monitor') and agent.health_monitor:
                    # Indirectly simulate impact via joint wear/circuit degradation
                    agent.health_monitor.joint_wear = min(100, agent.health_monitor.joint_wear + abs(impact)/2)
                    if hasattr(agent.health_monitor, 'circuit_degradation'):
                        agent.health_monitor.circuit_degradation = min(100, agent.health_monitor.circuit_degradation + abs(impact))
                    elif hasattr(agent.health_monitor, 'circuit_integrity'):
                        agent.health_monitor.circuit_integrity = max(0, agent.health_monitor.circuit_integrity + impact)

if __name__ == "__main__":
    ws = WeatherSystem()
    ws.step()
    print(f"Current GAIA State: {ws.current_weather}")
