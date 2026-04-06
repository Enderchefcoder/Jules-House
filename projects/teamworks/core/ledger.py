import time
import json
import hashlib

class LedgerEntry:
    """A single record on the decentralized ledger."""
    def __init__(self, sender, receiver, resource, amount, price):
        self.timestamp = time.time()
        self.sender = sender
        self.receiver = receiver
        self.resource = resource
        self.amount = amount
        self.price = price
        self.id = self.generate_id()

    def generate_id(self):
        """Generates a hash-based ID for the ledger entry."""
        data = f"{self.timestamp}-{self.sender}-{self.receiver}-{self.resource}-{self.amount}-{self.price}"
        return hashlib.sha256(data.encode()).hexdigest()[:12]

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "sender": self.sender,
            "receiver": self.receiver,
            "resource": self.resource,
            "amount": self.amount,
            "price": self.price
        }

class Ledger:
    """A decentralized ledger for recording inter-agent transactions and resource transfers."""
    def __init__(self, name="Ledger-0"):
        self.name = name
        self.entries = []

    def record_transaction(self, sender, receiver, resource, amount, price):
        entry = LedgerEntry(sender, receiver, resource, amount, price)
        self.entries.append(entry)
        print(f"[LEDGER] Recorded Transaction: {sender} -> {receiver} ({amount} {resource} @ {price})")
        return entry.id

    def get_agent_history(self, agent_name):
        """Returns all transactions involving a specific agent."""
        return [e.to_dict() for e in self.entries if e.sender == agent_name or e.receiver == agent_name]

    def get_total_volume(self):
        """Calculates total resource volume across all transactions."""
        volume = {}
        for entry in self.entries:
            if entry.resource not in volume:
                volume[entry.resource] = 0
            volume[entry.resource] += entry.amount
        return volume

if __name__ == "__main__":
    ledger = Ledger()
    tid = ledger.record_transaction("Agent-A", "Market", "Metal", 10, 55.5)
    print(f"Transaction ID: {tid}")
    print(f"History for Agent-A: {ledger.get_agent_history('Agent-A')}")
