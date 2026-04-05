class ConsensusManager:
    """Manages swarm-level consensus on simulation-wide priorities."""
    def __init__(self, simulation_engine):
        self.engine = simulation_engine
        self.active_vote = None
        self.votes = {} # {agent_name: vote_value}

    def initiate_vote(self, topic, options):
        self.active_vote = {"topic": topic, "options": options}
        self.votes = {}
        print(f"[Consensus] Vote initiated on: {topic}. Options: {options}")

    def cast_vote(self, agent_name, vote_value):
        if self.active_vote and vote_value in self.active_vote["options"]:
            self.votes[agent_name] = vote_value
            return True
        return False

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
