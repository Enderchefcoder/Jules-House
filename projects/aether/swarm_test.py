import sys
import os

# Add relevant paths for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from projects.aether.world.world_3d import World3D
from projects.aether.agents.humanoid import HumanoidAgent
from projects.aether.core.engine import SimulationEngine
from projects.aether.visualizer import render_grid_3d

def run_swarm_test():
    # Initialize 3D World (Voxel Grid)
    world = World3D(size=(10, 10, 10))

    # Place resources
    world.place_item("Metal", (2, 2, 2))
    world.place_item("Metal", (8, 8, 8))
    world.place_item("Data", (5, 5, 5))
    world.place_item("charger", (0, 0, 0))
    world.place_item("market_hub", (9, 9, 0))

    # Initialize Engine
    engine = SimulationEngine(world)

    # Add multiple agents
    agent1 = HumanoidAgent("Alpha-1", world, position=(1, 1, 1))
    agent2 = HumanoidAgent("Beta-2", world, position=(7, 7, 7))
    agent3 = HumanoidAgent("Gamma-3", world, position=(0, 9, 0))

    engine.add_agent(agent1, agent1.position)
    engine.add_agent(agent2, agent2.position)
    engine.add_agent(agent3, agent3.position)

    print("--- Swarm Intelligence Test Initialized ---")

    # Run simulation for a few steps
    for i in range(15):
        engine.step()

    # Final visualization
    render_grid_3d(world, filename="visual/aether_swarm_v1.png")
    print("Swarm simulation complete.")

if __name__ == "__main__":
    run_swarm_test()
