import collections

class PriorityMessageBus:
    """
    A scalable, priority-based message bus for the AETHER ecosystem.
    Supports publish-subscribe and priority levels (Emergency, High, Normal, Low).
    """
    def __init__(self, governor=None):
        self.queues = collections.defaultdict(list)
        self.subscribers = collections.defaultdict(list)
        self.collective_memory = {} # {resource_type: [pos1, pos2, ...]}
        self.priority_levels = {"Emergency": 0, "High": 1, "Normal": 2, "Low": 3}
        self.topic_keys = {"Emergency": "SECURE-KEY-2026", "Internal": "SWARM-ONLY"}
        self.relays = [] # List of ORION RelayBeacons
        self.global_state = {"vibe": 0.5, "sentiment": 0.5} # 2026 Sentiment Integration
        self.governor = governor

    def add_relay(self, relay):
        self.relays.append(relay)

    def subscribe(self, topic, agent_name):
        self.subscribers[topic].append(agent_name)

    def post(self, sender, content, type="Normal", priority="Normal", signed_by=None, origin_pos=None):
        # 2026 Security Filter: Check Governor's Quarantine List
        if self.governor and hasattr(self.governor, 'is_quarantined'):
            if self.governor.is_quarantined(sender):
                # print(f"[HERMES] BLOCKED message from quarantined agent: {sender}")
                return

        msg = {
            "sender": sender,
            "content": content,
            "type": type,
            "priority": priority,
            "signed_by": signed_by,
            "origin_pos": origin_pos,
            "step": None
        }
        p_val = self.priority_levels.get(priority, 2)
        self.queues[p_val].append(msg)

        # Auto-update collective memory for resource discoveries
        if type == "resource_discovery":
            res_type, pos = content
            if res_type not in self.collective_memory:
                self.collective_memory[res_type] = []
            if pos not in self.collective_memory[res_type]:
                self.collective_memory[res_type].append(pos)

    def query_memory(self, resource_type):
        return self.collective_memory.get(resource_type, [])

    def remove_from_memory(self, resource_type, pos):
        if resource_type in self.collective_memory and pos in self.collective_memory[resource_type]:
            self.collective_memory[resource_type].remove(pos)

    def get_messages(self, type=None, min_priority="Low", viewer_role="Standard", viewer_pos=None):
        """Retrieves messages filtered by type, priority, authorization, and range."""
        limit = self.priority_levels.get(min_priority, 3)
        all_msgs = []
        for p in range(limit + 1):
            all_msgs.extend(self.queues[p])

        filtered_msgs = []
        for m in all_msgs:
            # Topic Encryption Check (Simulated Authorization)
            if m["priority"] == "Emergency" and viewer_role not in ["Admin", "Governor", "EmergencyResponse"]:
                continue

            if type and m["type"] != type:
                continue

            # ORION Range Check
            if viewer_pos and m.get("origin_pos"):
                dist = sum(abs(a - b) for a, b in zip(viewer_pos, m["origin_pos"]))
                base_range = 10
                # Check for relay boost
                boost = 0
                for relay in self.relays:
                    if relay.is_active:
                        # If origin or viewer is near a relay, increase range
                        dist_to_origin = sum(abs(a - b) for a, b in zip(relay.position, m["origin_pos"]))
                        dist_to_viewer = sum(abs(a - b) for a, b in zip(relay.position, viewer_pos))
                        if dist_to_origin < 5 or dist_to_viewer < 5:
                            boost = max(boost, relay.range_boost)

                if dist > (base_range + boost):
                    continue # Message out of range

            filtered_msgs.append(m)

        return filtered_msgs

    def step(self, current_step, max_age=5):
        """Ticks the message bus, assigning steps and clearing old messages."""
        for p in self.queues:
            for m in self.queues[p]:
                if m["step"] is None:
                    m["step"] = current_step
        self.clear_old_messages(current_step, max_age)

    def clear_old_messages(self, current_step, max_age=5):
        for p in self.queues:
            self.queues[p] = [m for m in self.queues[p] if m["step"] is not None and current_step - m["step"] <= max_age]

if __name__ == "__main__":
    bus = PriorityMessageBus()
    bus.post("Agent1", "Help!", priority="Emergency")
    print(f"HERMES: {len(bus.get_messages())} messages in bus.")
