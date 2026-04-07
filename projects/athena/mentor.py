import random
import json

class MentorSystem:
    """
    Framework for agents to exchange 'Experience Packets' (brain weight deltas or discovered clusters).
    Enhances collective swarm intelligence.
    """
    def __init__(self, message_bus):
        self.message_bus = message_bus
        self.experience_log = []

    def log_mentorship(self, mentor, mentee, packet_type, content):
        """Logs a mentoring session."""
        entry = {
            "mentor": mentor,
            "mentee": mentee,
            "type": packet_type,
            "content": content,
            "timestamp": "2026-04-07"
        }
        self.experience_log.append(entry)
        if self.message_bus:
            self.message_bus.post("ATHENA-MENTOR", entry, type="mentorship_complete")
        print(f"[ATHENA] Mentorship Complete: {mentor} -> {mentee} ({packet_type})")

    def distribute_experience(self, agents):
        """Randomly selects agents to share knowledge based on performance or role."""
        if len(agents) < 2:
            return

        # Simple logic: Scouts share resource locations, Traders share market trends
        potential_mentors = [a for a in agents if a.role in ["Scout", "Trader", "Drone"]]
        potential_mentees = [a for a in agents if a.role in ["Gatherer", "Titan"]]

        if potential_mentors and potential_mentees:
            mentor = random.choice(potential_mentors)
            mentee = random.choice(potential_mentees)

            if mentor.role == "Drone" or mentor.role == "Scout":
                # Share mapped sectors or resource locations
                if hasattr(mentor, 'mapped_area'):
                    content = list(mentor.mapped_area)[:10] # Top 10 mapped points
                    self.log_mentorship(mentor.name, mentee.name, "Environmental Map", content)
                else:
                    # Generic resource locations
                    locs = mentor.shared_resource_locations if hasattr(mentor, 'shared_resource_locations') else {}
                    self.log_mentorship(mentor.name, mentee.name, "Resource Heatmap", locs)

            elif mentor.role == "Trader":
                # Share market trends (simulated weight delta for profit-maximizing decision)
                delta = {"target_profit_weight": 0.85}
                self.log_mentorship(mentor.name, mentee.name, "Brain Weight Delta", delta)

    def __repr__(self):
        return f"MentorSystem(Total Sessions: {len(self.experience_log)})"

if __name__ == "__main__":
    print("Project ATHENA: MentorSystem module loaded.")
