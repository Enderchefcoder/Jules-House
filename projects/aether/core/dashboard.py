class CivilizationDashboard:
    """
    Project AETHER: Swarm-Wide Industrial Telemetry.
    Tracks global metrics to monitor the progress toward the Industrial Zenith.
    """
    def __init__(self, engine):
        self.engine = engine
        self.total_alloy_produced = 0
        self.total_tasks_completed = 0
        self.avg_circuit_integrity = 100.0
        self.market_liquidity = 0.0
        self.active_infrastructure = {}

    def update_metrics(self, foundry_list=None):
        """Aggregates metrics from the simulation engine and agents."""
        # 1. Industrial Output
        if foundry_list:
            self.total_alloy_produced = sum(f.alloy_output for f in foundry_list)

        # 2. Swarm Health
        health_list = [a.health_monitor.get_overall_health() for a in self.engine.agents if hasattr(a, 'health_monitor') and a.health_monitor is not None]
        if health_list:
            self.avg_circuit_integrity = sum(health_list) / len(health_list)

        # 3. Task Throughput
        self.total_tasks_completed = sum(getattr(a, 'tasks_completed', 0) for a in self.engine.agents)

        # 4. Market Liquidity (Total balance in the swarm)
        self.market_liquidity = sum(getattr(a, 'balance', 0.0) for a in self.engine.agents)

        # 5. Infrastructure Count
        if hasattr(self.engine.world, 'items'):
            self.active_infrastructure = {}
            for item in self.engine.world.items.values():
                self.active_infrastructure[item] = self.active_infrastructure.get(item, 0) + 1

    def display_report(self):
        print("\n=== CIVILIZATION DASHBOARD: INDUSTRIAL ZENITH TELEMETRY ===")
        print(f"Total Alloy in Foundries: {self.total_alloy_produced}")
        print(f"Total Swarm Tasks Completed: {self.total_tasks_completed}")
        print(f"Average Swarm Health: {self.avg_circuit_integrity:.2f}%")
        print(f"Global Market Liquidity: {self.market_liquidity:.2f} Credits")
        print(f"Infrastructure: {self.active_infrastructure}")
        print("===========================================================\n")
