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
from projects.aether.core.consensus import ConsensusManager
from projects.teamworks.core.org_chart import OrgChart
from projects.teamworks.core.conflict_resolver import ConflictResolver
from projects.helios.grid import EnergyGrid
from projects.helios.solar_model import SolarModel

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

    # 5. Initialize New Systems (TeamWorks, HELIOS, Swarm Consensus)
    org_chart = OrgChart()
    conflict_resolver = ConflictResolver()
    consensus_manager = ConsensusManager(engine)
    energy_grid = EnergyGrid()
    solar_model = SolarModel()

    # 6. Add Specialized Agents
    agents = [
        HumanoidAgent("Scout-Alpha", world, position=(1, 1, 1), role="Scout"),
        HumanoidAgent("Gatherer-Beta", world, position=(7, 7, 7), role="Gatherer"),
        HumanoidAgent("Trader-Gamma", world, position=(0, 9, 0), role="Trader")
    ]

    for agent in agents:
        engine.add_agent(agent, agent.position)
        org_chart.assign_role(agent.name, agent.role)

    # Setup Hierarchy: Scout-Alpha is the Lead
    org_chart.add_subordinate("Scout-Alpha", "Gatherer-Beta")
    org_chart.add_subordinate("Scout-Alpha", "Trader-Gamma")

    print("\n--- 2026 Integrated Simulation: AETHER-TeamWorks-Feel-VERITAS-NEXUS-HELIOS ---")
    print(f"Agents Active: {[a.name for a in agents]}")
    print(f"Roles: {[a.role for a in agents]}")

    # 7. Run Simulation Steps
    for i in range(1, 11):
        engine.step()

        # Update HELIOS Energy Grid
        solar_model.update_weather()
        prod = solar_model.get_production()
        energy_grid.update_price(prod)

        # Periodically simulate sensory capture and signing (Feel AI + VERITAS)
        if i % 3 == 0:
            for agent in agents:
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

        # Periodically simulate Swarm Consensus (Vote on Mission Priority)
        if i % 5 == 0:
            consensus_manager.initiate_vote("Mission Priority", ["Energy Gathering", "Data Scavenging", "Market Expansion"])
            for agent in agents:
                # Mock voting logic
                vote = random.choice(["Energy Gathering", "Data Scavenging", "Market Expansion"])
                consensus_manager.cast_vote(agent.name, vote)
                print(f"[{agent.name}] Voted for: {vote}")
            consensus_manager.tally_results()

        # Mock resource contention check (using ConflictResolver)
        # If two agents are on the same tile (unlikely in this small test but here's the logic)
        positions = {}
        for agent in agents:
            if agent.position not in positions:
                positions[agent.position] = []
            positions[agent.position].append(agent)

        for pos, pos_agents in positions.items():
            if len(pos_agents) > 1 and world.get_item(pos) in ["Metal", "Data"]:
                print(f"[EVENT] Contention at {pos} between {[a.name for a in pos_agents]}!")
                winner = conflict_resolver.resolve_resource_conflict(pos_agents, pos)

    # 8. Final Output
    render_grid_3d(world, filename="visual/aether_integrated_test.png")
    print("\n--- Simulation Summary ---")
    for agent in engine.agents:
        print(agent)

    if engine.task_manager:
        print(f"Total Task Tickets: {len(engine.task_manager.tickets)}")
        for tid, ticket in engine.task_manager.tickets.items():
            print(f"- {ticket.title} ({ticket.status.value})")

    print("\n--- TeamWorks Organizational Summary ---")
    for lead, subs in org_chart.hierarchy.items():
        print(f"Lead: {lead} -> Subordinates: {subs}")

if __name__ == "__main__":
    run_integrated_sim()
