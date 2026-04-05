class OrgChart:
    """Manages agent hierarchies and reporting structures in TeamWorks."""
    def __init__(self):
        self.hierarchy = {} # {lead_name: [subordinate_names]}
        self.roles = {} # {agent_name: role}

    def assign_role(self, agent_name, role):
        self.roles[agent_name] = role
        print(f"[OrgChart] {agent_name} assigned role: {role}")

    def add_subordinate(self, lead_name, sub_name):
        if lead_name not in self.hierarchy:
            self.hierarchy[lead_name] = []
        if sub_name not in self.hierarchy[lead_name]:
            self.hierarchy[lead_name].append(sub_name)
            print(f"[OrgChart] {sub_name} is now subordinate to {lead_name}")

    def get_lead(self, sub_name):
        for lead, subs in self.hierarchy.items():
            if sub_name in subs:
                return lead
        return None

    def get_subordinates(self, lead_name):
        return self.hierarchy.get(lead_name, [])

if __name__ == "__main__":
    oc = OrgChart()
    oc.assign_role("Scout-Alpha", "Lead")
    oc.add_subordinate("Scout-Alpha", "Gatherer-Beta")
    print(f"Lead of Gatherer-Beta: {oc.get_lead('Gatherer-Beta')}")
