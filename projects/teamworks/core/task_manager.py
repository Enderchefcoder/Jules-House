import uuid
import time
from enum import Enum

class TaskStatus(Enum):
    OPEN = "open"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    COMPLETE = "complete"
    FAILED = "failed"

class TaskTicket:
    """A single unit of work in the TeamWorks ecosystem."""
    def __init__(self, title, description, priority=3):
        self.id = str(uuid.uuid4())[:8]
        self.title = title
        self.description = description
        self.priority = priority # 1 (High) to 5 (Low)
        self.status = TaskStatus.OPEN
        self.assignee = None
        self.created_at = time.time()
        self.history = []

    def update_status(self, new_status, reason=None):
        self.status = new_status
        self.history.append({
            "status": new_status.value,
            "timestamp": time.time(),
            "reason": reason
        })
        return True

    def __repr__(self):
        return f"TaskTicket({self.id}, {self.title}, Status: {self.status.value}, Assignee: {self.assignee})"

class TaskManager:
    """Handles ticket-based task tracking and assignment for agent swarms."""
    def __init__(self):
        self.tickets = {} # {ticket_id: TaskTicket}

    def create_ticket(self, title, description, priority=3):
        ticket = TaskTicket(title, description, priority)
        self.tickets[ticket.id] = ticket
        print(f"Created ticket: {ticket.id} - {title}")
        return ticket.id

    def assign_ticket(self, ticket_id, agent_name):
        if ticket_id in self.tickets:
            ticket = self.tickets[ticket_id]
            ticket.assignee = agent_name
            ticket.update_status(TaskStatus.ASSIGNED, f"Assigned to {agent_name}")
            print(f"Assigned ticket {ticket_id} to {agent_name}")
            return True
        return False

    def list_open_tickets(self):
        return [t for t in self.tickets.values() if t.status == TaskStatus.OPEN]

    def list_tickets_by_agent(self, agent_name):
        return [t for t in self.tickets.values() if t.assignee == agent_name]

    def reassign_tasks_for_agent(self, agent_name):
        """Re-opens all tasks assigned to an agent that has gone offline."""
        count = 0
        for ticket in self.tickets.values():
            if ticket.assignee == agent_name and ticket.status != TaskStatus.COMPLETE:
                ticket.assignee = None
                ticket.update_status(TaskStatus.OPEN, f"Re-opened: Agent {agent_name} went offline.")
                count += 1
        return count

if __name__ == "__main__":
    tm = TaskManager()
    tid = tm.create_ticket("Resource Scavenging", "Collect 10 Metal and 5 Data from Sector 7G.")
    tm.assign_ticket(tid, "Alpha-01")
    print(tm.tickets[tid])
    print(f"Open Tickets: {tm.list_open_tickets()}")
