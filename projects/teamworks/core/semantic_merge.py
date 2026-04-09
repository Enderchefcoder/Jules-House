class ConflictMerger:
    """
    A semantic conflict resolution engine for agent swarms.
    Resolves overlapping agent actions based on role priority, battery urgency, and economic status.
    """
    def __init__(self):
        self.resolved_conflicts = 0
        self.priority_map = {
            "Scout": 3,
            "Drone": 2,
            "Trader": 1,
            "Gatherer": 4, # Higher is more critical for task completion
            "Titan": 5     # Construction takes highest priority
        }

    def resolve_action_conflict(self, agents, action_type):
        """
        Takes a list of agents competing for the same action (e.g., claiming a resource, building an outpost).
        Returns the winning agent.
        """
        if not agents:
            return None
        if len(agents) == 1:
            return agents[0]

        # Criteria 1: Role Priority
        # Criteria 2: Physical Health (VITA) - healthy agents preferred for tasks
        # Criteria 3: Battery Urgency (lower battery = more urgent if it's a critical task)
        # Criteria 4: Economic Status (lower balance = more need for the resource)

        def score_agent(a):
            role_score = self.priority_map.get(a.role, 0) * 10
            # Safety check: health_monitor might be None even if hasattr returns True
            health_score = 5.0
            if hasattr(a, 'health_monitor') and a.health_monitor is not None:
                health_score = a.health_monitor.get_overall_health() / 10.0
            battery_score = (100 - a.battery) / 20.0
            balance_score = (1000 - a.balance) / 100.0 if hasattr(a, 'balance') else 0

            # Project ATHENA: Experience bonus
            experience_score = 0
            if hasattr(a, 'experience_packets'):
                experience_score = len(getattr(a, 'experience_packets')) * 2

            return role_score + health_score + battery_score + balance_score + experience_score

        # Sort agents by score
        agents.sort(key=score_agent, reverse=True)
        winner = agents[0]

        self.resolved_conflicts += 1
        print(f"[TEAMWORKS-MERGE] Resolved '{action_type}' conflict for {len(agents)} agents. Winner: {winner.name}")
        return winner

    def merge_task_claims(self, tickets, claims):
        """
        Resolves multiple agents claiming the same task tickets.
        claims: {ticket_id: [agent1, agent2, ...]}
        """
        resolved_claims = {}
        for ticket_id, agents in claims.items():
            if len(agents) > 1:
                winner = self.resolve_action_conflict(agents, f"Task Claim: {ticket_id}")
                resolved_claims[ticket_id] = winner
            else:
                resolved_claims[ticket_id] = agents[0]
        return resolved_claims

if __name__ == "__main__":
    print("TeamWorks: ConflictMerger module loaded.")
