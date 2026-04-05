import random

class ConflictResolver:
    """Resolves resource contention using a priority-based lottery."""
    def __init__(self):
        self.active_conflicts = []

    def resolve_resource_conflict(self, agents, resource_pos):
        """
        Given a list of agents competing for a resource, determine the winner.
        Priority-based: Agents with higher 'priority' scores have higher odds.
        """
        if not agents:
            return None

        # Calculate weights based on agent role/priority
        weights = []
        for agent in agents:
            weight = 1.0
            if hasattr(agent, 'role'):
                if agent.role == "Gatherer":
                    weight = 2.0
                elif agent.role == "Scout":
                    weight = 0.5
            weights.append(weight)

        winner = random.choices(agents, weights=weights, k=1)[0]
        print(f"[ConflictResolver] Conflict at {resource_pos} resolved. Winner: {winner.name}")
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
