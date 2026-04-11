import sys
import os
import random

# Add relevant paths for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from projects.chronos.market import Market
from projects.aether.world.world_3d import World3D
from projects.aether.agents.humanoid import HumanoidAgent
from projects.aether.agents.titan import HumanoidTitan
from projects.zephyr.drone import DroneAgent
from projects.nemesis.rogue import RogueAgent
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
from projects.aegis.firewall import SwarmFirewall
from projects.vita.repair_bay import RepairBay
from projects.gaia.weather import WeatherSystem
from projects.gaia.ecosystem import EcosystemManager
from projects.vulcan.foundry import Foundry
from projects.orion.relay import RelayBeacon
from projects.hydra.distributor import BrainDistributor

def run_integrated_sim():
    # 1. Initialize 3D World (Voxel Grid) - Scaled for 2026 demands
    world = World3D(size=(20, 20, 20), use_atlas=True)

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

    # Place VITA Repair Bays
    world.place_item("repair_bay", (5, 0, 5))
    world.place_item("repair_bay", (15, 19, 15))

    # Place VULCAN Foundries
    foundry_1_pos = (10, 0, 10)
    foundry_2_pos = (0, 10, 10)
    world.place_item("foundry", foundry_1_pos)
    world.place_item("foundry", foundry_2_pos)

    # Place ORION Relays
    world.place_item("relay_station", (10, 10, 10))
    world.place_item("relay_station", (5, 15, 10))

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
    market = Market()
    org_chart = OrgChart()
    conflict_resolver = ConflictResolver()
    conflict_merger = ConflictMerger() # TeamWorks Intent Merging
    consensus_manager = ConsensusManager(engine)
    governor = SwarmGovernor(engine)
    ledger = Ledger()
    energy_grid = EnergyGrid()
    solar_model = SolarModel()
    argus = Satellite()
    gaia_weather = WeatherSystem()
    gaia_ecosystem = EcosystemManager(world)
    mentor_system = MentorSystem(engine.message_bus) # ATHENA
    firewall = SwarmFirewall() # AEGIS
    repair_bay_1 = RepairBay((5, 0, 5))
    repair_bay_2 = RepairBay((15, 19, 15))

    # Initialize VULCAN, ORION, HYDRA integration
    foundry_1 = Foundry(foundry_1_pos)
    foundry_2 = Foundry(foundry_2_pos)
    relay_1 = RelayBeacon((10, 10, 10))
    relay_2 = RelayBeacon((5, 15, 10))
    engine.message_bus.add_relay(relay_1)
    engine.message_bus.add_relay(relay_2)
    brain_distributor = BrainDistributor(compute_market) # HYDRA

    # 6. Add Specialized Agents - Scaled Swarm with TITAN, ZEPHYR, and NEMESIS Rogue
    # Pass brain_distributor and market to humanoid agents
    agents = [
        HumanoidAgent("Scout-Alpha", world, position=(1, 1, 1), role="Scout", market=market, message_bus=engine.message_bus, brain_distributor=brain_distributor),
        HumanoidAgent("Scout-Delta", world, position=(18, 18, 18), role="Scout", market=market, message_bus=engine.message_bus, brain_distributor=brain_distributor),
        HumanoidAgent("Gatherer-Beta", world, position=(10, 10, 10), role="Gatherer", market=market, message_bus=engine.message_bus, brain_distributor=brain_distributor),
        HumanoidAgent("Gatherer-Epsilon", world, position=(2, 17, 3), role="Gatherer", market=market, message_bus=engine.message_bus, brain_distributor=brain_distributor),
        HumanoidAgent("Trader-Gamma", world, position=(0, 14, 0), role="Trader", market=market, message_bus=engine.message_bus, brain_distributor=brain_distributor),
        HumanoidAgent("Trader-Zeta", world, position=(19, 2, 19), role="Trader", market=market, message_bus=engine.message_bus, brain_distributor=brain_distributor),
        HumanoidTitan("Titan-01", world, position=(5, 5, 5), market=market, message_bus=engine.message_bus),
        DroneAgent("Zephyr-01", world, position=(10, 10, 19)), # ZEPHYR Drone
        DroneAgent("Zephyr-02", world, position=(5, 5, 15)),
        RogueAgent("NEMESIS-Rogue", world, position=(0, 0, 19)) # NEMESIS Rogue
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

    # 7. Run Simulation Steps - Extended for deeper emergence
    for i in range(1, 501):
        engine.step()

        # Update ARGUS Global Monitoring
        event = argus.scan_globe()
        if event:
            print(f"[ARGUS] ALERT: {event['name']} - {event['desc']}")
            governor.reconcile_shocks(argus.current_vibe)

        # 2026 Sentiment Update
        health_list = [a.health_monitor.get_overall_health() for a in agents if hasattr(a, 'health_monitor') and a.health_monitor is not None]
        avg_agent_health = sum(health_list) / len(health_list) if health_list else 100.0
        agent_stress = (100 - avg_agent_health) / 100.0

        # Update Market Sentiment
        if hasattr(engine.message_bus, 'global_state'):
            vibe = argus.get_sentiment_metric()
            engine.message_bus.global_state["vibe"] = vibe

            # Update CHRONOS Market Sentiment
            market.update_sentiment(vibe, [1.0 - (a.health_monitor.get_overall_health()/100.0) for a in agents if hasattr(a, 'health_monitor') and a.health_monitor is not None])

            # Sync MessageBus state with Market state
            engine.message_bus.global_state["sentiment"] = market.market_sentiment

        # Update GAIA Environment
        gaia_weather.step()
        gaia_weather.apply_effects(agents)
        gaia_ecosystem.step()

        # Update HELIOS Energy Grid
        prod = solar_model.get_production(gaia_weather=gaia_weather) * argus.get_solar_modifier()
        energy_grid.update_price(prod)

        # VULCAN: Deep Integration - Check for agents at foundries
        for agent in agents:
            if hasattr(agent, 'inventory') and agent.inventory.get("Metal", 0) > 0:
                if agent.position == foundry_1.position:
                    m = agent.inventory["Metal"]
                    foundry_1.deposit_resources(metal=m, energy=10) # Simulated energy deposit
                    agent.inventory["Metal"] = 0
                    print(f"[VULCAN] {agent.name} deposited {m} Metal at Foundry 1.")
                elif agent.position == foundry_2.position:
                    m = agent.inventory["Metal"]
                    foundry_2.deposit_resources(metal=m, energy=10)
                    agent.inventory["Metal"] = 0
                    print(f"[VULCAN] {agent.name} deposited {m} Metal at Foundry 2.")

        # Alloy collection logic - Enhanced for robustness
        current_foundry = None
        if agent.position == foundry_1.position:
            current_foundry = foundry_1
        elif agent.position == foundry_2.position:
            current_foundry = foundry_2

        if current_foundry and current_foundry.alloy_output > 0:
            current_inv = sum(agent.inventory.values())
            space = agent.inventory_capacity - current_inv
            if space > 0:
                collected = current_foundry.collect_alloy(min(space, current_foundry.alloy_output))
                agent.inventory["Alloy"] = agent.inventory.get("Alloy", 0) + collected
                print(f"[VULCAN] {agent.name} collected {collected} ALLOY.")

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
            # Ensure we have enough agents to sample from
            valid_agents = [a for a in agents if hasattr(a, 'role') and a.role != "Drone"]
            if len(valid_agents) >= 3:
                competing_agents = random.sample(valid_agents, 3)
                winner = conflict_merger.resolve_action_conflict(competing_agents, "Task Claim")

        # VULCAN: Process foundries
        if i % 25 == 0:
            foundry_1.process()
            foundry_2.process()

        # HYDRA: Distributed Inference requests (Now mostly handled within HumanoidAgent.perform_task)
        if i % 30 == 0:
            # Periodic manual test request
            brain_distributor.request_inference("Scout-Alpha", [0]*8)

        # Security Check: AEGIS + Governor Integration
        if i % 5 == 0:
            for rogue in [a for a in agents if a.role == "Rogue"]:
                if rogue.name in firewall.blocked_senders:
                    governor.quarantine_agent(rogue.name)

    # 8. Final Output
    render_grid_3d(world, filename="visual/aether_complex_v7.png")
    print("\n--- Ecosystem Summary ---")
    print(f"Total Steps: {i}")
    print(f"ATHENA Sessions: {len(mentor_system.experience_log)}")
    print(f"TeamWorks Merges: {conflict_merger.resolved_conflicts}")

    for agent in engine.agents:
        print(agent)

if __name__ == "__main__":
    run_integrated_sim()
