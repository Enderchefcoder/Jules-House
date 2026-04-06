import random

class ConflictResolver:
    """Resolves resource contention using a priority-based lottery."""
    def __init__(self):
        self.active_conflicts = []

    def resolve_resource_conflict(self, agents, resource_pos):
        """
        Given a list of agents competing for a resource, determine the winner.
        Priority-based: Agents with higher 'priority' scores have higher odds.
        Now considers battery levels (desperation) and role-based seniority.
        """
        if not agents:
            return None

        # Calculate weights based on agent role/priority
        weights = []
        for agent in agents:
            # Base weight by role
            weight = 1.0
            if hasattr(agent, 'role'):
                if agent.role == "Gatherer":
                    weight = 3.0
                elif agent.role == "Scout":
                    weight = 1.0
                elif agent.role == "Trader":
                    weight = 2.0

            # Desperation factor: Lower battery increases urgency (up to +2.0 weight)
            if hasattr(agent, 'battery'):
                desperation = (100 - agent.battery) / 50.0
                weight += desperation

            # Seniority factor: High balance agents (successful traders) have slight edge
            if hasattr(agent, 'balance'):
                seniority = min(2.0, agent.balance / 1000.0)
                weight += seniority

            weights.append(max(0.1, weight))

        winner = random.choices(agents, weights=weights, k=1)[0]
        print(f"[ConflictResolver] Contention at {resource_pos} resolved.")
        print(f"  - Participants: {[(a.name, w) for a, w in zip(agents, weights)]}")
        print(f"  - Winner: {winner.name}")
        return winner

if __name__ == "__main__":
    class MockAgent:
        def __init__(self, name, role):
            self.name = name
            self.role = role

    cr = ConflictResolver()
    a1 = MockAgent("Agent-1", "Scout")
    a2 = MockAgent("Agent-2", "Gatherer")
    winner = cr.resolve_resource_conflict([a1, a2], (5,5,5))
    print(f"Winner: {winner.name}")
