import sys
import os

# Add relevant paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from world.world_3d import World3D
from agents.humanoid import HumanoidAgent
from core.engine import SimulationEngine
from visualizer import render_grid_3d

def run_integrated_test():
    print("Initializing Integrated AETHER+CHRONOS Simulation...")

    # 1. Setup World
    world = World3D(size=(10, 10, 10))
    world.place_item('charger', (0, 0, 0))
    world.place_item('market_hub', (5, 5, 0))
    world.place_item('Metal', (2, 2, 1))
    world.place_item('Data', (8, 8, 2))
    world.place_item('obstacle', (5, 5, 1))

    # 2. Setup Engine
    engine = SimulationEngine(world)

    # 3. Add Agent
    agent = HumanoidAgent("AETHER-01", world, position=(0, 0, 0))
    # Give some initial resources and low battery to trigger behaviors
    agent.battery = 40
    engine.add_agent(agent, (0, 0, 0))

    print(f"Initial State: {agent}")

    # 4. Run steps
    for i in range(5):
        engine.step()
        print(f"Agent State: {agent}")
        # Render state at each step to visual/aether_integrated_test_step_{i}.png
        render_grid_3d(world, f"visual/aether_integrated_test_step_{i}.png")

    print("\nIntegrated Test Complete.")

if __name__ == "__main__":
    run_integrated_test()
