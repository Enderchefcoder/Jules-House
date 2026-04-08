import collections

class PriorityMessageBus:
    """
    A scalable, priority-based message bus for the AETHER ecosystem.
    Supports publish-subscribe and priority levels (Emergency, High, Normal, Low).
    """
    def __init__(self):
        self.queues = collections.defaultdict(list)
        self.subscribers = collections.defaultdict(list)
        self.collective_memory = {} # {resource_type: [pos1, pos2, ...]}
        self.priority_levels = {"Emergency": 0, "High": 1, "Normal": 2, "Low": 3}
        self.topic_keys = {"Emergency": "SECURE-KEY-2026", "Internal": "SWARM-ONLY"}

    def subscribe(self, topic, agent_name):
        self.subscribers[topic].append(agent_name)

    def post(self, sender, content, type="Normal", priority="Normal", signed_by=None):
        msg = {
            "sender": sender,
            "content": content,
            "type": type,
            "priority": priority,
            "signed_by": signed_by,
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

    def get_messages(self, type=None, min_priority="Low", viewer_role="Standard"):
        """Retrieves messages filtered by type, priority, and authorization."""
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
