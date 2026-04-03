import time

class SimulationEngine:
    """The central engine that manages the AETHER simulation."""

    def __init__(self, world):
        self.world = world
        self.agents = []
        self.current_step = 0
        self.is_running = False

    def add_agent(self, agent, position):
        """Adds an agent to the simulation at the specified position."""
        if self.world.place_agent(agent, position):
            self.agents.append(agent)
            return True
        return False

    def step(self):
        """Executes a single step in the simulation."""
        self.current_step += 1
        print(f"\n--- Simulation Step {self.current_step} ---")

        for agent in self.agents:
            # Simple behavior: agent moves randomly if it has energy
            agent.perform_task()

        # In a real simulation, we might update world state here
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
