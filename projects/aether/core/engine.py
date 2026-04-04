import time
import sys
import os

# Try to import market from chronos
try:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
    from chronos.market import Market
except ImportError:
    Market = None

class SimulationEngine:
    """The central engine that manages the AETHER simulation, now with a Market."""

    def __init__(self, world):
        self.world = world
        self.is_3d = hasattr(world, 'depth')
        self.agents = []
        self.current_step = 0
        self.is_running = False
        self.market = Market() if Market else None

    def add_agent(self, agent, position):
        """Adds an agent to the simulation at the specified position."""
        if self.world.place_agent(agent, position):
            self.agents.append(agent)
            # Link agent to market if not already linked
            if hasattr(agent, 'market') and agent.market is None:
                agent.market = self.market
            return True
        return False

    def step(self):
        """Executes a single step in the simulation."""
        self.current_step += 1
        print(f"\n--- Simulation Step {self.current_step} ---")

        # Fluctuate market each step
        if self.market:
            self.market.fluctuate()
            print(f"Market Prices: {self.market.resources}")

        for agent in self.agents:
            agent.perform_task()

        return True

    def run(self, max_steps=10):
        """Runs the simulation for a set number of steps."""
        self.is_running = True
        try:
            for _ in range(max_steps):
                if not self.is_running:
                    break
                self.step()
                time.sleep(0.1) # Simulate time passing
        except KeyboardInterrupt:
            print("\nSimulation stopped by user.")
        finally:
            self.is_running = False
            print(f"\nSimulation ended at step {self.current_step}.")

if __name__ == "__main__":
    print("SimulationEngine module loaded.")
