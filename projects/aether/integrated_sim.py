import sys
import os
import random

# Add relevant paths for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from projects.aether.world.world_3d import World3D
from projects.aether.agents.humanoid import HumanoidAgent
from projects.aether.agents.titan import HumanoidTitan
from projects.aether.core.engine import SimulationEngine
from projects.aether.visualizer import render_grid_3d
from projects.nexus.node import NexusNode, ComputeMarket
from projects.aether.core.consensus import ConsensusManager
from projects.teamworks.core.org_chart import OrgChart
from projects.teamworks.core.conflict_resolver import ConflictResolver
from projects.teamworks.core.governor import SwarmGovernor
from projects.teamworks.core.ledger import Ledger
from projects.helios.grid import EnergyGrid
from projects.helios.solar_model import SolarModel
from projects.argus.satellite import Satellite

def run_integrated_sim():
    # 1. Initialize 3D World (Voxel Grid) - Scaled for 2026 demands
    world = World3D(size=(20, 20, 20))

    # 2. Setup Resources and Hubs - Increased density
    resource_positions = [
        (2, 2, 2), (8, 8, 8), (5, 5, 5), (12, 12, 12), (3, 10, 4),
        (10, 3, 10), (7, 7, 2), (1, 14, 5), (14, 1, 10), (6, 6, 6),
        (18, 18, 18), (15, 5, 15), (5, 15, 5), (19, 1, 2), (2, 19, 18)
    ]
    for i, pos in enumerate(resource_positions):
        res = "Metal" if i % 2 == 0 else "Data"
        world.place_item(res, pos)

    world.place_item("charger", (0, 0, 0))
    world.place_item("charger", (19, 19, 19))
    world.place_item("market_hub", (10, 10, 0))
    world.place_item("market_hub", (19, 0, 19))

    # 3. Setup NEXUS Compute Market with diverse nodes
    nodes = [
        NexusNode("StandardNode", node_type="Standard"),
        NexusNode("HighComputeNode", node_type="High-Compute"),
        NexusNode("LowPowerNode", node_type="Low-Power")
    ]
    compute_market = ComputeMarket(nodes)

    # 4. Initialize Simulation Engine
    engine = SimulationEngine(world)

    # 5. Initialize New Systems (TeamWorks, HELIOS, Swarm Consensus, ARGUS)
    org_chart = OrgChart()
    conflict_resolver = ConflictResolver()
    consensus_manager = ConsensusManager(engine)
    governor = SwarmGovernor(engine)
    ledger = Ledger()
    energy_grid = EnergyGrid()
    solar_model = SolarModel()
    argus = Satellite()

    # 6. Add Specialized Agents - Scaled Swarm with TITAN
    agents = [
        HumanoidAgent("Scout-Alpha", world, position=(1, 1, 1), role="Scout"),
        HumanoidAgent("Scout-Delta", world, position=(18, 18, 18), role="Scout"),
        HumanoidAgent("Gatherer-Beta", world, position=(10, 10, 10), role="Gatherer"),
        HumanoidAgent("Gatherer-Epsilon", world, position=(2, 17, 3), role="Gatherer"),
        HumanoidAgent("Trader-Gamma", world, position=(0, 14, 0), role="Trader"),
        HumanoidAgent("Trader-Zeta", world, position=(19, 2, 19), role="Trader"),
        HumanoidTitan("Titan-01", world, position=(5, 5, 5))
    ]

    for agent in agents:
        engine.add_agent(agent, agent.position)
        org_chart.assign_role(agent.name, agent.role)

    # Setup Hierarchy: Scout-Alpha is the Lead
    org_chart.add_subordinate("Scout-Alpha", "Gatherer-Beta")
    org_chart.add_subordinate("Scout-Alpha", "Trader-Gamma")

    print("\n--- 2026 Integrated Simulation: AETHER-TeamWorks-Feel-VERITAS-NEXUS-HELIOS-ARGUS ---")
    print(f"Agents Active: {[a.name for a in agents]}")

    # 7. Run Simulation Steps - Extended for depth
    for i in range(1, 101):
        engine.step()

        # Update ARGUS Global Monitoring
        event = argus.scan_globe()
        if event:
            print(f"[ARGUS] ALERT: {event['name']} - {event['desc']}")
            governor.reconcile_shocks(argus.current_vibe)

        # Update HELIOS Energy Grid
        solar_model.update_weather()
        prod = solar_model.get_production() * argus.get_solar_modifier()
        energy_grid.update_price(prod)

        # Periodically simulate sensory capture and signing (Feel AI + VERITAS)
        if i % 5 == 0:
            for agent in agents:
                mock_img = f"visual/aether_integrated_test.png"
                if os.path.exists(mock_img):
                    packet = agent.sensory_system.capture_observation(mock_img, "steady_hum")
                    if packet:
                        print(f"[{agent.name}] Captured signed observation: {packet['mood_classification']} (SIG: {packet['signature'][:8]}...)")

        # Periodically simulate NEXUS compute transactions
        if i % 6 == 0:
            for agent in agents:
                cost = compute_market.get_inference_cost() * argus.get_market_modifier()
                if agent.balance >= cost:
                    if compute_market.request_compute(agent.name, 10, 8, cost):
                        agent.balance -= cost
                        ledger.record_transaction(agent.name, "NEXUS-MARKET", "Compute", 1, cost)
                        print(f"[{agent.name}] Purchased remote brain inference from NEXUS. Balance: {agent.balance:.2f}")

        # Periodically simulate Swarm Consensus (Vote on Mission Priority)
        if i % 10 == 0:
            consensus_manager.initiate_vote("Mission Priority", ["Energy Gathering", "Data Scavenging", "Market Expansion"])
            for agent in agents:
                # Mock voting logic
                vote = random.choice(["Energy Gathering", "Data Scavenging", "Market Expansion"])
                consensus_manager.cast_vote(agent.name, vote)
            winner = consensus_manager.tally_results()
            if winner:
                governor.apply_policy("Mission Priority", winner)

        # Contention at Resource locations
        positions = {}
        for agent in agents:
            if agent.position not in positions:
                positions[agent.position] = []
            positions[agent.position].append(agent)

        for pos, pos_agents in positions.items():
            if len(pos_agents) > 1 and world.get_item(pos) in ["Metal", "Data"]:
                print(f"[EVENT] Contention at {pos}!")
                winner = conflict_resolver.resolve_resource_conflict(pos_agents, pos)

    # 8. Final Output
    render_grid_3d(world, filename="visual/aether_complex_v1.png")
    print("\n--- Simulation Summary ---")
    for agent in engine.agents:
        print(agent)

    print(f"\nTotal Transaction Volume: {ledger.get_total_volume()}")
    print("\n--- TeamWorks Organizational Summary ---")
    for lead, subs in org_chart.hierarchy.items():
        print(f"Lead: {lead} -> Subordinates: {subs}")

if __name__ == "__main__":
    run_integrated_sim()
