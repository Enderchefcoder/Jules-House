import sys
import os
import random

# Add relevant paths for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from projects.aether.world.world_3d import World3D
from projects.aether.agents.humanoid import HumanoidAgent
from projects.aether.core.engine import SimulationEngine
from projects.aether.visualizer import render_grid_3d
from projects.nexus.node import NexusNode, ComputeMarket

def run_integrated_sim():
    # 1. Initialize 3D World (Voxel Grid)
    world = World3D(size=(10, 10, 10))

    # 2. Setup Resources and Hubs
    world.place_item("Metal", (2, 2, 2))
    world.place_item("Metal", (8, 8, 8))
    world.place_item("Data", (5, 5, 5))
    world.place_item("charger", (0, 0, 0))
    world.place_item("market_hub", (9, 9, 0))

    # 3. Setup NEXUS Compute Market
    nodes = [NexusNode(f"ComputeNode-{i}") for i in range(3)]
    compute_market = ComputeMarket(nodes)

    # 4. Initialize Simulation Engine
    engine = SimulationEngine(world)

    # 5. Add Specialized Agents
    agents = [
        HumanoidAgent("Scout-Alpha", world, position=(1, 1, 1), role="Scout"),
        HumanoidAgent("Gatherer-Beta", world, position=(7, 7, 7), role="Gatherer"),
        HumanoidAgent("Trader-Gamma", world, position=(0, 9, 0), role="Trader")
    ]

    for agent in agents:
        engine.add_agent(agent, agent.position)

    print("--- 2026 Integrated Simulation: AETHER-TeamWorks-Feel-VERITAS-NEXUS ---")
    print(f"Agents Active: {[a.name for a in agents]}")
    print(f"Roles: {[a.role for a in agents]}")

    # 6. Run Simulation Steps
    for i in range(10):
        engine.step()

        # Periodically simulate sensory capture and signing (Feel AI + VERITAS)
        if i % 3 == 0:
            for agent in agents:
                # In a real sim, we'd take a screenshot, but here we'll mock the path
                mock_img = f"visual/aether_swarm_v1.png"
                if os.path.exists(mock_img):
                    packet = agent.sensory_system.capture_observation(mock_img, "steady_hum")
                    if packet:
                        print(f"[{agent.name}] Captured signed observation: {packet['mood_classification']} (SIG: {packet['signature'][:8]}...)")

        # Periodically simulate NEXUS compute transactions
        if i % 4 == 0:
            for agent in agents:
                cost = compute_market.get_inference_cost()
                if agent.balance >= cost:
                    if compute_market.request_compute(agent.name, 10, 8, cost):
                        agent.balance -= cost
                        print(f"[{agent.name}] Purchased remote brain inference from NEXUS. Balance: {agent.balance:.2f}")

    # 7. Final Output
    render_grid_3d(world, filename="visual/aether_integrated_test.png")
    print("\n--- Simulation Summary ---")
    for agent in engine.agents:
        print(agent)

    if engine.task_manager:
        print(f"Total Task Tickets: {len(engine.task_manager.tickets)}")
        for tid, ticket in engine.task_manager.tickets.items():
            print(f"- {ticket.title} ({ticket.status.value})")

if __name__ == "__main__":
    run_integrated_sim()
