import random
import torch
import torch.optim as optim
import torch.nn.functional as F
from utils.pathfinding import a_star
from core.brain import RobotBrain

# Try to import market from chronos
try:
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
    from chronos.market import Market
    from feel_ai.multimodal_encoder import MultimodalEncoder
    from veritas.integrity import IntegrityManager
    from aegis.firewall import SwarmFirewall
    from vita.health import HealthMonitor
except ImportError:
    Market = None
    MultimodalEncoder = None
    IntegrityManager = None
    SwarmFirewall = None
    HealthMonitor = None

class SensorySystem:
    """An integrated sensory system that captures and signs agent observations."""
    def __init__(self, agent_name):
        self.encoder = MultimodalEncoder() if MultimodalEncoder else None
        self.integrity = IntegrityManager() if IntegrityManager else None
        self.agent_name = agent_name
        self.last_packet = None

    def capture_observation(self, world_snapshot_path, audio_vibe):
        if not self.encoder:
            return None

        packet = self.encoder.generate_packet(world_snapshot_path, audio_vibe)
        packet["agent"] = self.agent_name

        if self.integrity:
            import json
            signature = self.integrity.sign_data(json.dumps(packet))
            packet["signature"] = signature

        self.last_packet = packet
        return packet

class HumanoidAgent:
    """A humanoid robot agent for the AETHER simulation with RL and infrastructure hooks."""

    def __init__(self, name, world, position=(0, 0), market=None, message_bus=None, role="Generalist", brain_distributor=None):
        self.name = name
        self.world = world
        self.position = position
        self.battery = 100
        self.status = "Idle"
        self.is_3d = hasattr(world, 'depth')
        self.brain = RobotBrain(input_size=8 if self.is_3d else 6)
        self.optimizer = optim.Adam(self.brain.parameters(), lr=0.01)
        self.role = role

        # Specialized attributes based on role
        self.battery_cost = 5
        self.inventory_capacity = 1
        self.market_multiplier = 1.0

        if role == "Scout":
            self.battery_cost = 2
        elif role == "Gatherer":
            self.inventory_capacity = 10
        elif role == "Trader":
            self.market_multiplier = 1.25

        # Economic attributes
        self.inventory = {"Metal": 0, "Data": 0, "Alloy": 0}
        self.balance = 500.0  # Starting capital
        self.market = market
        self.message_bus = message_bus
        self.task_manager = None
        self.brain_distributor = brain_distributor
        self.shared_resource_locations = {} # {resource_type: [pos1, pos2]}
        self.sensory_system = SensorySystem(self.name)
        self.health_monitor = HealthMonitor(self.name) if HealthMonitor else None
        self.firewall = SwarmFirewall() if SwarmFirewall else None
        self.tasks_completed = 0

        # Path Caching (Optimization)
        self.current_path = []
        self.current_target = None

    def receive_experience(self, mentor_name, exp_type, data):
        """Incorporate an experience packet (e.g., neural weights) from another agent."""
        if exp_type == "Neural Distillation":
            # Apply distilled weights to current brain
            with torch.no_grad():
                current_weights = self.brain.state_dict()
                for k, v in data.items():
                    if k in current_weights:
                        # Soft update: current = 0.9*current + 0.1*mentor
                        current_weights[k] = current_weights[k] * 0.9 + v
                self.brain.load_state_dict(current_weights)
            print(f"[{self.name}] Integrated Neural Distillation from {mentor_name}.")

    def reward_feedback(self, reward, target_idx):
        """Perform a single RL step based on a decision reward with battery-sensitive scaling."""
        if hasattr(self, 'last_state') and self.last_state is not None:
             self.optimizer.zero_grad()
             output = self.brain(self.last_state)

             # 2026 Cognitive Refinement: Scale reward by battery status
             # Positive rewards are more significant when battery is high (efficiency focus)
             # Penalties are more severe when battery is low (survival focus)
             battery_modifier = self.battery / 100.0 if reward > 0 else (2.0 - (self.battery / 100.0))
             scaled_reward = reward * battery_modifier

             # One-hot target
             target = output.clone().detach()
             target[target_idx] += scaled_reward
             loss = F.mse_loss(output, target)
             loss.backward()
             self.optimizer.step()
             # print(f"[{self.name}] RL Update: Reward {reward:.1f}, Loss {loss.item():.4f}")

    def broadcast_emergency(self, level, message):
        """Broadcasts an emergency message to the swarm."""
        if self.message_bus:
            # Check if using HERMES (PriorityMessageBus)
            if hasattr(self.message_bus, 'priority_levels'):
                 self.message_bus.post(self.name, f"[{level}] {message}", type="emergency", priority="Emergency", origin_pos=self.position)
            else:
                 self.message_bus.post(self.name, f"[{level}] {message}", type="emergency")
            print(f"{self.name} BROADCAST EMERGENCY: {message}")

    def move(self, dx, dy):
        """Moves the agent on the world grid."""
        if self.battery < self.battery_cost:
            print(f"{self.name} battery too low to move!")
            return False

        new_pos = (self.position[0] + dx, self.position[1] + dy)
        # Handle 3D coordinates if necessary
        if self.is_3d and len(new_pos) == 2:
            new_pos = (new_pos[0], new_pos[1], self.position[2])

        if self.world.move_agent(self, self.position, new_pos):
            self.position = new_pos
            self.battery -= self.battery_cost
            self.status = "Moving"
            if self.health_monitor:
                self.health_monitor.step(movement_type="Standard")
            return True
        return False

    def move_3d(self, dx, dy, dz):
        """Moves the agent in 3D space."""
        # Calculate effective battery cost (reduced near Outpost Beacons)
        effective_cost = self.battery_cost
        current_item = self.world.get_item(self.position)
        if current_item == "outpost_beacon":
            effective_cost = max(1, self.battery_cost // 2)

        if self.battery < effective_cost:
            print(f"{self.name} battery too low to move!")
            return False
        new_pos = (self.position[0] + dx, self.position[1] + dy, self.position[2] + dz)
        if self.world.move_agent(self, self.position, new_pos):
            self.position = new_pos
            self.battery -= effective_cost
            self.status = "Moving 3D"
            if self.health_monitor:
                self.health_monitor.step(movement_type="Heavy" if self.role == "Titan" else "Standard")
            return True
        return False

    def recharge(self, amount=25):
        """Simulates recharging the agent. Costs money if a market is present."""
        if self.market:
            price_per_unit = self.market.get_price("Energy") / 10.0 # Scaling price
            # Traders get a discount on energy
            if self.role == "Trader":
                price_per_unit *= 0.8
            cost = amount * price_per_unit
            if self.balance >= cost:
                self.balance -= cost
                self.battery = min(100, self.battery + amount)
                self.status = f"Recharging (Cost: {cost:.2f})"
                print(f"{self.name} recharged to {self.battery}%. Balance: {self.balance:.2f}")
                return True
            else:
                self.status = "Insolvent - Cannot Recharge"
                print(f"{self.name} cannot afford recharge!")
                return False
        else:
            self.battery = min(100, self.battery + amount)
            self.status = "Recharging"
            return True

    def find_nearest_item(self, item_types):
        """Scans the world for the nearest item of certain types."""
        if isinstance(item_types, str):
            item_types = [item_types]

        min_dist = float('inf')
        nearest = None

        # Access world items
        if self.is_3d:
            items_to_check = self.world.items.items()
        else:
            items_to_check = []
            for y in range(self.world.height):
                for x in range(self.world.width):
                    it = self.world.get_item((x, y))
                    if it:
                        items_to_check.append(((x, y), it))

        for pos, itype in items_to_check:
            if itype in item_types:
                dist = sum(abs(a - b) for a, b in zip(self.position, pos))
                if dist < min_dist:
                    min_dist = dist
                    nearest = pos
        return nearest

    def process_messages(self):
        """Checks the message bus for updates from other agents with ORION range logic."""
        if not self.message_bus:
            return

        # Use position for range-based filtering if HERMES is present
        messages = self.message_bus.get_messages(type="resource_discovery", viewer_pos=self.position)
        for m in messages:
            if m["sender"] != self.name:
                # AEGIS Firewall Check
                if self.firewall and not self.firewall.validate_message(m["sender"], m["content"], "resource_discovery"):
                    continue

                res_type, pos = m["content"]
                if res_type not in self.shared_resource_locations:
                    self.shared_resource_locations[res_type] = []
                if pos not in self.shared_resource_locations[res_type]:
                    self.shared_resource_locations[res_type].append(pos)
                    # print(f"{self.name} received broadcast: {res_type} at {pos}")

    def perform_task(self):
        """Decides and performs an action based on state, battery, and RL feedback."""
        # 0. Process swarm communication
        self.process_messages()

        # 1. Check current tile for collection or interaction
        current_item = self.world.get_item(self.position)

        # Maintenance Check (Project VITA)
        if current_item == "outpost_beacon" or current_item == "market_hub":
             if self.health_monitor and self.health_monitor.get_overall_health() < 80:
                  if self.inventory.get("Metal", 0) >= 5 and self.balance >= 100:
                      self.inventory["Metal"] -= 5
                      self.balance -= 100
                      self.health_monitor.perform_repair("Full")
                      print(f"[{self.name}] Performed self-maintenance. Health restored.")
                      self.status = "Maintenance Complete"
                      return

        if current_item in ["Metal", "Data", "Alloy"]:
            if sum(self.inventory.values()) < self.inventory_capacity:
                self.inventory[current_item] += 1
                self.tasks_completed += 1
                if hasattr(self.world, 'remove_item'):
                    self.world.remove_item(self.position)

                # RL Reward for collection
                if hasattr(self, 'last_decision_idx'):
                    self.reward_feedback(1.0, self.last_decision_idx)

                if self.message_bus:
                    priority = "High" if self.role == "Scout" else "Normal"
                    self.message_bus.post(self.name, (current_item, self.position), type="resource_discovery", priority=priority, origin_pos=self.position)
                    # print(f"{self.name} broadcasting discovery: {current_item} at {self.position}")

                print(f"{self.name} collected {current_item}. Inventory: {self.inventory}")
                self.status = f"Collected {current_item}"
                return
            else:
                self.status = "Inventory Full"

        if current_item == "repair_bay":
            if self.health_monitor:
                if self.balance >= 200:
                    self.balance -= 200
                    self.health_monitor.perform_repair("Full")
                    print(f"[{self.name}] Professional repair at REPAIR BAY. Balance: {self.balance:.2f}")
                    self.status = "Hardware Restored"
                    return

        if current_item == "market_hub":
            if self.market:
                total_sale = 0
                for res, amt in self.inventory.items():
                    if amt > 0:
                        price = self.market.get_price(res) * self.market_multiplier
                        total_sale += price * amt
                        self.inventory[res] = 0
                if total_sale > 0:
                    self.balance += total_sale
                    self.tasks_completed += 1
                    # RL Reward for sale
                    if hasattr(self, 'last_decision_idx'):
                        self.reward_feedback(2.0, self.last_decision_idx)
                    print(f"{self.name} sold inventory for {total_sale:.2f}. Balance: {self.balance:.2f}")
                    self.status = f"Sold Goods (+{total_sale:.2f})"
                    return

        if current_item == "charger" and self.battery < 90:
            if not self.recharge():
                 # RL Penalty for failure to recharge
                 if hasattr(self, 'last_decision_idx'):
                    self.reward_feedback(-0.5, self.last_decision_idx)
            return

        # 2. Decide Target using RobotBrain
        survival_need = (100 - self.battery) / 100.0
        profit_need = sum(self.inventory.values()) / self.inventory_capacity
        task_need = 0.5
        health_need = (100 - self.health_monitor.get_overall_health()) / 100.0 if self.health_monitor else 0.0
        role_map = {"Scout": 0.1, "Gatherer": 0.5, "Trader": 0.9, "Generalist": 0.0, "Titan": 1.0}
        role_scaled = role_map.get(self.role, 0.0)
        balance_scaled = min(1.0, self.balance / 2000.0)

        if self.is_3d:
            brain_input = torch.tensor([survival_need, profit_need, task_need, health_need, role_scaled, balance_scaled, 0.0, 0.0])
        else:
            brain_input = torch.tensor([survival_need, profit_need, task_need, health_need, role_scaled, balance_scaled])

        self.last_state = brain_input

        # HYDRA Offloading logic: Call remote compute if battery is low
        if self.battery < 40 and self.brain_distributor:
            self.brain_distributor.request_inference(self.name, brain_input)
            # print(f"[{self.name}] HYDRA: Offloaded inference to NEXUS.")

        decision_weights = self.brain.forward(brain_input)
        self.last_decision_idx = torch.argmax(decision_weights).item()

        # Target Selection logic
        charger_pos = self.find_nearest_item("charger")
        market_pos = self.find_nearest_item("market_hub")
        repair_pos = self.find_nearest_item("repair_bay")

        options = []
        if charger_pos: options.append((decision_weights[0].item(), charger_pos, "Charging"))
        if market_pos: options.append((decision_weights[1].item(), market_pos, "Selling"))

        task_target = None
        if self.message_bus and hasattr(self.message_bus, 'query_memory'):
            for res in ["Metal", "Data"]:
                m_locs = self.message_bus.query_memory(res)
                if m_locs:
                    task_target = m_locs[0]
                    if self.world.get_item(task_target) != res:
                        self.message_bus.remove_from_memory(res, task_target)
                        task_target = None
                    else: break

        if task_target: options.append((decision_weights[2].item(), task_target, "Task"))
        resource_pos = self.find_nearest_item(["Metal", "Data"])
        if resource_pos: options.append((decision_weights[3].item(), resource_pos, "Scavenging"))
        if repair_pos: options.append((decision_weights[5].item(), repair_pos, "Maintenance"))

        target = None
        if options:
            options.sort(key=lambda x: x[0], reverse=True)
            target = options[0][1]

            # Absolute Overrides
            if self.battery < 20 and charger_pos:
                target = charger_pos
            elif self.health_monitor and self.health_monitor.get_overall_health() < 30 and repair_pos:
                target = repair_pos

        if target:
            if self.position == target:
                self.status = f"At {self.world.get_item(target)}"
                self.current_path = []
                self.current_target = None
                return

            if target != self.current_target or not self.current_path:
                self.current_target = target
                self.current_path = a_star(self.world, self.position, target)
                if self.current_path and self.current_path[0] == self.position:
                    self.current_path.pop(0)

            if self.current_path:
                next_step = self.current_path.pop(0)
                dist = sum(abs(a - b) for a, b in zip(self.position, next_step))
                if dist > 1:
                    self.current_path = a_star(self.world, self.position, target)
                    if self.current_path and self.current_path[0] == self.position:
                        self.current_path.pop(0)
                    if self.current_path: next_step = self.current_path.pop(0)
                    else: next_step = None

                if next_step:
                    dx, dy = next_step[0] - self.position[0], next_step[1] - self.position[1]
                    if self.is_3d:
                        self.move_3d(dx, dy, next_step[2] - self.position[2])
                    else:
                        self.move(dx, dy)
                    self.status = f"Heading to {target}"
                    return

        # RL Penalty for Idling
        self.reward_feedback(-0.1, self.last_decision_idx)
        moves = [(0,1,0), (0,-1,0), (1,0,0), (-1,0,0), (0,0,1), (0,0,-1)] if self.is_3d else [(0,1), (0,-1), (1,0), (-1,0)]
        random.shuffle(moves)
        for m in moves:
            if self.is_3d:
                if self.move_3d(*m): return
            else:
                if self.move(*m): return
        self.status = "Idling"

    def __repr__(self):
        health_str = f", Health: {self.health_monitor.get_overall_health():.1f}%" if self.health_monitor else ""
        return f"HumanoidAgent({self.name}, {self.position}, Bat: {self.battery}%, Bal: {self.balance:.2f}{health_str})"

if __name__ == "__main__":
    print("HumanoidAgent module loaded.")
