import time
import sys
import os

# Try to import market from chronos
try:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
    from chronos.market import Market
    from aether.core.hazards import HazardManager
    from teamworks.core.task_manager import TaskManager
    from teamworks.core.heartbeat import HeartbeatManager
    from projects.hermes.bus import PriorityMessageBus
except ImportError:
    Market = None
    HazardManager = None
    TaskManager = None
    HeartbeatManager = None
    PriorityMessageBus = None

class SimulationEngine:
    """The central engine that manages the AETHER simulation, now with a Market and MessageBus."""

    def __init__(self, world):
        self.world = world
        self.is_3d = hasattr(world, 'depth')
        self.agents = []
        self.current_step = 0
        self.is_running = False
        self.market = Market() if Market else None
        self.message_bus = PriorityMessageBus() if PriorityMessageBus else None
        self.hazard_manager = HazardManager(world) if HazardManager else None
        self.task_manager = TaskManager() if TaskManager else None
        self.heartbeat_manager = HeartbeatManager(task_manager=self.task_manager) if HeartbeatManager else None
        if self.heartbeat_manager:
            self.heartbeat_manager.start()

    def add_agent(self, agent, position):
        """Adds an agent to the simulation at the specified position."""
        if self.world.place_agent(agent, position):
            self.agents.append(agent)
            # Link agent to market if not already linked
            if hasattr(agent, 'market') and agent.market is None:
                agent.market = self.market
            # Register with heartbeat
            if self.heartbeat_manager:
                self.heartbeat_manager.register_agent(agent.name)
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

        # Update message bus (Encapsulated)
        if self.message_bus:
            if hasattr(self.message_bus, 'step'):
                self.message_bus.step(self.current_step)
            elif hasattr(self.message_bus, 'clear_old_messages'):
                # Fallback for old message bus
                 for m in getattr(self.message_bus, 'messages', []):
                    if m["step"] is None:
                        m["step"] = self.current_step
                 self.message_bus.clear_old_messages(self.current_step)

        # Inject message bus and pulse heartbeat
        for agent in self.agents:
            if hasattr(agent, 'message_bus') and agent.message_bus is None:
                agent.message_bus = self.message_bus

            if self.heartbeat_manager:
                # Only pulse if agent has battery
                if hasattr(agent, 'battery') and agent.battery > 0:
                    self.heartbeat_manager.pulse(agent.name)

            # Inject Task Manager
            if hasattr(agent, 'task_manager') and agent.task_manager is None:
                agent.task_manager = self.task_manager

            agent.perform_task()

        # Update hazards
        if self.hazard_manager:
            self.hazard_manager.step(self.agents)

        # Distribute Tasks if items found
        if self.task_manager:
            items_to_check = []
            if hasattr(self.world, 'items'):
                # World3D
                items_to_check = self.world.items.items()
            elif hasattr(self.world, 'items_grid'):
                # WorldGrid (2D)
                for y in range(self.world.height):
                    for x in range(self.world.width):
                        it = self.world.get_item((x, y))
                        if it:
                            items_to_check.append(((x, y), it))

            for pos, item_type in items_to_check:
                if item_type in ["Metal", "Data"]:
                    # Create a ticket if one doesn't exist for this location
                    title = f"Scavenge {item_type} at {pos}"
                    exists = any(t.title == title for t in self.task_manager.tickets.values())
                    if not exists:
                        self.task_manager.create_ticket(title, f"Retrieve {item_type} from coordinates {pos}", priority=2)

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
            if self.heartbeat_manager:
                self.heartbeat_manager.stop()
            print(f"\nSimulation ended at step {self.current_step}.")

if __name__ == "__main__":
    print("SimulationEngine module loaded.")
