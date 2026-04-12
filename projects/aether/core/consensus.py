try:
    from projects.veritas.integrity import IntegrityManager
except ImportError:
    IntegrityManager = None

class ConsensusManager:
    """Manages swarm-level consensus on simulation-wide priorities with VERITAS integrity."""
    def __init__(self, simulation_engine, secret_key=None):
        self.engine = simulation_engine
        self.active_vote = None
        self.votes = {} # {agent_name: vote_value}
        self.integrity_manager = IntegrityManager(secret_key=secret_key) if IntegrityManager else None

    def initiate_vote(self, topic, options):
        self.active_vote = {"topic": topic, "options": options}
        self.votes = {}
        print(f"[Consensus] Vote initiated on: {topic}. Options: {options}")

    def cast_vote(self, agent_name, vote_value, signature=None):
        if not self.active_vote or vote_value not in self.active_vote["options"]:
            return False

        # VERITAS: Enforce signature verification if integrity manager is present
        if self.integrity_manager:
            if not signature:
                print(f"[Consensus] REJECTED: Missing signature from {agent_name}")
                return False
            import json
            # Use sort_keys=True for deterministic serialization
            vote_data = json.dumps({"agent": agent_name, "vote": vote_value, "topic": self.active_vote["topic"]}, sort_keys=True)
            if not self.integrity_manager.verify_data(vote_data, signature):
                print(f"[Consensus] REJECTED: Invalid signature from {agent_name}")
                return False

        self.votes[agent_name] = vote_value
        return True

    def tally_results(self):
        if not self.active_vote or not self.votes:
            return None

        counts = {option: 0 for option in self.active_vote["options"]}
        for vote in self.votes.values():
            counts[vote] += 1

        winner = max(counts, key=counts.get)
        print(f"[Consensus] Vote complete for '{self.active_vote['topic']}'. Result: {winner}")
        self.active_vote = None
        return winner

if __name__ == "__main__":
    cm = ConsensusManager(None)
    cm.initiate_vote("Energy vs Research", ["Energy", "Research"])
    cm.cast_vote("Agent-1", "Energy")
    cm.cast_vote("Agent-2", "Research")
    cm.cast_vote("Agent-3", "Energy")
    cm.tally_results()
