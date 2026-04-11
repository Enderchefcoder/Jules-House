import random
import time

class Satellite:
    """
    Project ARGUS: Autonomous Remote Global Urban Simulation.
    Simulates global monitoring and event generation to influence the AETHER ecosystem.
    """
    def __init__(self):
        self.events = []
        self.current_vibe = "Stable"
        self.global_sentiment = 0.5 # 0.0 (Panic) to 1.0 (Euphoria)
        self.geopolitical_tension = 0.5 # 0.0 to 1.0

    def scan_globe(self):
        """Simulates a global scan for significant 2026 events."""
        scenarios = [
            {"type": "weather_shift", "name": "Solar Flare", "impact": "High", "sentiment": 0.3, "desc": "Increased solar output, lowering energy prices but causing static glitches."},
            {"type": "market_crash", "name": "Compute Shortage", "impact": "Critical", "sentiment": 0.1, "desc": "NEXUS compute prices skyrocket due to hardware bottlenecks."},
            {"type": "geopolitical_shock", "name": "Border Closure", "impact": "Medium", "sentiment": 0.2, "desc": "Trade routes restricted, increasing resource scarcity."},
            {"type": "tech_breakthrough", "name": "Neuromorphic Efficiency", "impact": "Positive", "sentiment": 0.9, "desc": "Brain inference costs reduced across the board."},
            {"type": "market_boom", "name": "Market Optimism", "impact": "High", "sentiment": 0.8, "desc": "Positive projections lead to increased investment in autonomous trade."},
            {"type": "energy_crisis", "name": "Energy Grid Strain", "impact": "Critical", "sentiment": 0.15, "desc": "High demand and low production cause rolling brownouts in simulation sectors."}
        ]

        if random.random() < 0.3: # 30% chance of a major event per scan
            event = random.choice(scenarios)
            event["timestamp"] = time.time()
            self.events.append(event)
            self.current_vibe = event["name"]
            self.global_sentiment = event.get("sentiment", 0.5)
            return event
        return None

    def get_sentiment_metric(self):
        """Returns the current global sentiment for integration with AETHER brains."""
        return self.global_sentiment

    def get_market_modifier(self):
        """Returns a multiplier for CHRONOS market based on global state."""
        if self.current_vibe == "Compute Shortage":
            return 2.0
        if self.current_vibe == "Border Closure":
            return 1.5
        return 1.0

    def get_solar_modifier(self):
        """Returns a multiplier for HELIOS solar production."""
        if self.current_vibe == "Solar Flare":
            return 2.5
        return 1.0

if __name__ == "__main__":
    argus = Satellite()
    print("ARGUS Satellite System Online.")
    for _ in range(5):
        event = argus.scan_globe()
        if event:
            print(f"[EVENT DETECTED] {event['name']}: {event['desc']}")
        else:
            print("Globe scan: No significant anomalies.")
        time.sleep(0.1)
