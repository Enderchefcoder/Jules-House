class BrainDistributor:
    """
    Project HYDRA: Distributed Brain Inference.
    Allows agents to offload complex RobotBrain computations to NEXUS High-Compute nodes.
    """
    def __init__(self, compute_market, governor=None):
        self.compute_market = compute_market
        self.offload_log = []
        self.governor = governor

    def request_inference(self, agent_name, state_tensor, priority="Normal"):
        """Requests remote inference via the NEXUS market."""
        # Use Governor's quota if available, otherwise fallback to local infinity
        current_quota = self.governor.compute_quota if self.governor else float('inf')

        if current_quota <= 0:
            print(f"[HYDRA] Failed to offload inference for {agent_name}: GLOBAL QUOTA EXCEEDED.")
            return False

        # Map complexity to CPU/RAM requirements
        cpu_req = 10
        ram_req = 8
        reward = self.compute_market.get_inference_cost() * 2

        success = self.compute_market.request_compute(agent_name, cpu_req, ram_req, reward)
        if success:
            if self.governor:
                self.governor.compute_quota -= 1
                print(f"[HYDRA] Offloaded inference for {agent_name} to NEXUS market. Remaining Quota: {self.governor.compute_quota}")
            else:
                print(f"[HYDRA] Offloaded inference for {agent_name} to NEXUS market.")
            self.offload_log.append((agent_name, "NEXUS-Market"))
            return True # Simulated success
        else:
            print(f"[HYDRA] Failed to offload inference for {agent_name}: No suitable NEXUS node or insufficient credits.")
            return False

    def __repr__(self):
        return f"BrainDistributor(Log Entries: {len(self.offload_log)})"
