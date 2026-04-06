import uuid
import time
import random

class NexusNode:
    """A single compute node in the decentralized NEXUS network."""
    def __init__(self, name=None, node_type="Standard"):
        self.id = str(uuid.uuid4())[:8]
        self.name = name or f"Node-{self.id}"
        self.node_type = node_type

        # Base capacities
        self.cpu_capacity = random.randint(10, 100)
        self.ram_capacity = random.randint(8, 128)

        # Specialized scaling
        if node_type == "High-Compute":
            self.cpu_capacity *= 2
            self.ram_capacity = int(self.ram_capacity * 1.5)
        elif node_type == "Low-Power":
            self.cpu_capacity = int(self.cpu_capacity * 0.5)
            self.ram_capacity = int(self.ram_capacity * 0.5)

        self.bandwidth = random.randint(100, 1000) # Mbps
        self.current_load = {"cpu": 0, "ram": 0}
        self.peers = []
        self.tasks = []
        self.balance = 1000.0 # NEXUS Credits

    def register_peer(self, peer_node):
        if peer_node.id != self.id and peer_node not in self.peers:
            self.peers.append(peer_node)
            print(f"[{self.name}] Registered peer: {peer_node.name}")

    def accept_task(self, task_name, cpu_req, ram_req, reward):
        """Accepts a task if capacity allows and the reward is worth it."""
        if (self.current_load["cpu"] + cpu_req <= self.cpu_capacity and
            self.current_load["ram"] + ram_req <= self.ram_capacity):

            # Specialized heuristics
            if self.node_type == "High-Compute" and reward < 25:
                return False # High-Compute nodes are expensive, ignore low rewards

            if self.node_type == "Low-Power" and ram_req > 32:
                return False # Low-Power nodes cannot handle memory-heavy tasks

            # Simple heuristic for acceptance
            if reward > (cpu_req * 0.5 + ram_req * 0.2):
                self.current_load["cpu"] += cpu_req
                self.current_load["ram"] += ram_req
                self.tasks.append({
                    "name": task_name,
                    "cpu": cpu_req,
                    "ram": ram_req,
                    "reward": reward,
                    "status": "Running"
                })
                print(f"[{self.name}] Accepted task: {task_name}. Reward: {reward}")
                return True
        return False

    def complete_tasks(self):
        """Simulates completion of all running tasks."""
        for task in self.tasks:
            if task["status"] == "Running":
                self.balance += task["reward"]
                self.current_load["cpu"] -= task["cpu"]
                self.current_load["ram"] -= task["ram"]
                task["status"] = "Complete"
                print(f"[{self.name}] Completed task: {task['name']}. Balance: {self.balance:.2f}")
        self.tasks = [t for t in self.tasks if t["status"] != "Complete"]

    def __repr__(self):
        return f"NexusNode({self.name}, CPU: {self.cpu_capacity}, RAM: {self.ram_capacity}, Bal: {self.balance:.2f})"

class ComputeMarket:
    """Simulates a market for compute resources."""
    def __init__(self, nodes):
        self.nodes = nodes

    def request_compute(self, requester_name, cpu_req, ram_req, credits_offered):
        """Attempts to place a compute task on an available node."""
        for node in self.nodes:
            if node.accept_task(f"Remote_{requester_name}", cpu_req, ram_req, credits_offered):
                return True
        return False

    def get_inference_cost(self):
        return 2.5 # Credits per RobotBrain inference

    def get_pathfinding_cost(self, distance):
        return distance * 0.1 # Credits per unit of distance

def run_nexus_test():
    # Initialize network
    nodes = [NexusNode(f"Worker-{i}") for i in range(3)]

    # Register peers
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if i != j:
                nodes[i].register_peer(nodes[j])

    # Simulate task broadcasting and bidding
    print("\n--- NEXUS Task Distribution Test ---")
    tasks_to_distribute = [
        ("Agent Inference", 20, 16, 50),
        ("Dataset Analysis", 40, 64, 150),
        ("Vision Encoding", 15, 8, 30),
        ("Swarm Coordination", 10, 4, 15)
    ]

    for task in tasks_to_distribute:
        # Simple random peer selection for task offer
        offered = False
        potential_workers = nodes.copy()
        random.shuffle(potential_workers)

        for node in potential_workers:
            if node.accept_task(*task):
                offered = True
                break

        if not offered:
            print(f"[ALARM] Task {task[0]} could not be placed due to insufficient resources or low reward.")

    # Run network cycle
    print("\n--- NEXUS Cycle Completion ---")
    for node in nodes:
        node.complete_tasks()
        print(node)

if __name__ == "__main__":
    run_nexus_test()
