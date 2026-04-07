import sys
import os
import random

# Add relevant paths for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from projects.aether.world.world_3d import World3D
from projects.aether.agents.humanoid import HumanoidAgent
from projects.aether.agents.titan import HumanoidTitan
from projects.zephyr.drone import DroneAgent
from projects.athena.mentor import MentorSystem
from projects.aether.core.engine import SimulationEngine
from projects.aether.visualizer import render_grid_3d
from projects.nexus.node import NexusNode, ComputeMarket
from projects.aether.core.consensus import ConsensusManager
from projects.teamworks.core.org_chart import OrgChart
from projects.teamworks.core.conflict_resolver import ConflictResolver
from projects.teamworks.core.semantic_merge import ConflictMerger
from projects.teamworks.core.governor import SwarmGovernor
from projects.teamworks.core.ledger import Ledger
from projects.helios.grid import EnergyGrid
from projects.helios.solar_model import SolarModel
from projects.argus.satellite import Satellite

def run_integrated_sim():
    # 1. Initialize 3D World (Voxel Grid) - Scaled for 2026 demands
    world = World3D(size=(20, 20, 20))

    # 2. Setup Resources and Hubs - Increased density for longer sim
    resource_positions = [
        (2, 2, 2), (8, 8, 8), (5, 5, 5), (12, 12, 12), (3, 10, 4),
        (10, 3, 10), (7, 7, 2), (1, 14, 5), (14, 1, 10), (6, 6, 6),
        (18, 18, 18), (15, 5, 15), (5, 15, 5), (19, 1, 2), (2, 19, 18),
        (10, 10, 15), (15, 10, 10), (5, 19, 5), (19, 5, 19), (0, 10, 19)
    ]
    for i, pos in enumerate(resource_positions):
        res = "Metal" if i % 2 == 0 else "Data"
        world.place_item(res, pos)

    world.place_item("charger", (0, 0, 0))
    world.place_item("charger", (19, 19, 19))
    world.place_item("market_hub", (10, 10, 0))
    world.place_item("market_hub", (19, 0, 19))

    # 3. Setup NEXUS Compute Market
    nodes = [
        NexusNode("StandardNode", node_type="Standard"),
        NexusNode("HighComputeNode", node_type="High-Compute"),
        NexusNode("LowPowerNode", node_type="Low-Power")
    ]
    compute_market = ComputeMarket(nodes)

    # 4. Initialize Simulation Engine
    engine = SimulationEngine(world)

    # 5. Initialize Core Systems (TeamWorks, HELIOS, Swarm Consensus, ARGUS, ATHENA)
    org_chart = OrgChart()
    conflict_resolver = ConflictResolver()
    conflict_merger = ConflictMerger() # TeamWorks Intent Merging
    consensus_manager = ConsensusManager(engine)
    governor = SwarmGovernor(engine)
    ledger = Ledger()
    energy_grid = EnergyGrid()
    solar_model = SolarModel()
    argus = Satellite()
    mentor_system = MentorSystem(engine.message_bus) # ATHENA

    # 6. Add Specialized Agents - Scaled Swarm with TITAN and ZEPHYR Drones
    agents = [
        HumanoidAgent("Scout-Alpha", world, position=(1, 1, 1), role="Scout"),
        HumanoidAgent("Scout-Delta", world, position=(18, 18, 18), role="Scout"),
        HumanoidAgent("Gatherer-Beta", world, position=(10, 10, 10), role="Gatherer"),
        HumanoidAgent("Gatherer-Epsilon", world, position=(2, 17, 3), role="Gatherer"),
        HumanoidAgent("Trader-Gamma", world, position=(0, 14, 0), role="Trader"),
        HumanoidAgent("Trader-Zeta", world, position=(19, 2, 19), role="Trader"),
        HumanoidTitan("Titan-01", world, position=(5, 5, 5)),
        DroneAgent("Zephyr-01", world, position=(10, 10, 19)), # ZEPHYR Drone
        DroneAgent("Zephyr-02", world, position=(5, 5, 15))
    ]

    for agent in agents:
        engine.add_agent(agent, agent.position)
        if hasattr(agent, 'role'):
            org_chart.assign_role(agent.name, agent.role)

    # Setup Hierarchy
    org_chart.add_subordinate("Scout-Alpha", "Gatherer-Beta")
    org_chart.add_subordinate("Scout-Alpha", "Trader-Gamma")

    print("\n--- 2026 Integrated Ecosystem: ZEPHYR-ATHENA-AETHER-TeamWorks-HELIOS-ARGUS ---")
    print(f"Agents Active: {[a.name for a in agents]}")

    # 7. Run Simulation Steps - Extended to 150 for deeper emergence
    for i in range(1, 151):
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

        # Periodically simulate sensory capture (Feel AI + VERITAS)
        if i % 10 == 0:
            for agent in [a for a in agents if hasattr(a, 'sensory_system')]:
                mock_img = f"visual/aether_complex_v1.png"
                if os.path.exists(mock_img):
                    packet = agent.sensory_system.capture_observation(mock_img, "steady_hum")
                    if packet:
                        print(f"[{agent.name}] Signed Sensory Packet: {packet['mood_classification']}")

        # ATHENA: Mentorship cycles
        if i % 15 == 0:
            mentor_system.distribute_experience(agents)

        # TeamWorks: Conflict Merging (Intent)
        if i % 20 == 0:
            # Simulate a task claim conflict
            task_id = f"Critical-Resource-{i}"
            competing_agents = random.sample([a for a in agents if a.role != "Drone"], 3)
            winner = conflict_merger.resolve_action_conflict(competing_agents, "Task Claim")

    # 8. Final Output
    render_grid_3d(world, filename="visual/aether_complex_v2.png")
    print("\n--- Ecosystem Summary ---")
    print(f"Total Steps: {i}")
    print(f"ATHENA Sessions: {len(mentor_system.experience_log)}")
    print(f"TeamWorks Merges: {conflict_merger.resolved_conflicts}")

    for agent in engine.agents:
        print(agent)

if __name__ == "__main__":
    run_integrated_sim()
