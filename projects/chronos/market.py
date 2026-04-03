import random

class Market:
    """A central market that tracks resource prices."""
    def __init__(self):
        self.resources = {"Metal": 50, "Energy": 20, "Data": 100}
        self.history = {res: [val] for res, val in self.resources.items()}

    def get_price(self, resource):
        return self.resources.get(resource, 0)

    def fluctuate(self):
        """Simulates market price changes."""
        for res in self.resources:
            change = random.uniform(0.9, 1.1)
            self.resources[res] = max(1, round(self.resources[res] * change, 2))
            self.history[res].append(self.resources[res])

class TradeAgent:
    """An agent that trades resources on the market."""
    def __init__(self, name, market, balance=1000):
        self.name = name
        self.market = market
        self.balance = balance
        self.inventory = {"Metal": 0, "Energy": 0, "Data": 0}

    def produce(self, resource, amount):
        """Produces a resource at a cost (simplified)."""
        cost = amount * 5 # Flat cost for now
        if self.balance >= cost:
            self.balance -= cost
            self.inventory[resource] += amount
            return True
        return False

    def sell(self, resource, amount):
        """Sells a resource to the market."""
        if self.inventory[resource] >= amount:
            price = self.market.get_price(resource)
            revenue = price * amount
            self.inventory[resource] -= amount
            self.balance += revenue
            return True
        return False

    def buy(self, resource, amount):
        """Buys a resource from the market."""
        price = self.market.get_price(resource)
        cost = price * amount
        if self.balance >= cost:
            self.balance -= cost
            self.inventory[resource] += amount
            return True
        return False

    def __repr__(self):
        return f"TradeAgent({self.name}, Balance: {self.balance:.2f}, Inv: {self.inventory})"

if __name__ == "__main__":
    m = Market()
    a = TradeAgent("Trader1", m)

    print(f"Initial: {a}")
    a.produce("Metal", 10)
    print(f"After Production: {a}")

    m.fluctuate()
    print(f"Market Prices: {m.resources}")

    a.sell("Metal", 5)
    print(f"After Sale: {a}")
