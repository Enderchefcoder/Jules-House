import time
import threading

class HeartbeatManager:
    """Manages agent activation cycles and system pulse."""
    def __init__(self, interval=5.0, task_manager=None):
        self.interval = interval
        self.agents = {} # {agent_name: last_pulse}
        self.task_manager = task_manager
        self.running = False
        self._thread = None

    def register_agent(self, agent_name):
        self.agents[agent_name] = time.time()
        print(f"Registered agent {agent_name} with HeartbeatManager.")

    def pulse(self, agent_name):
        if agent_name in self.agents:
            self.agents[agent_name] = time.time()
            return True
        return False

    def check_health(self, timeout=10.0):
        current_time = time.time()
        unhealthy = []
        for name, last_pulse in self.agents.items():
            if current_time - last_pulse > timeout:
                unhealthy.append(name)
        return unhealthy

    def start(self):
        self.running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        print("HeartbeatManager started.")

    def _run_loop(self):
        while self.running:
            unhealthy = self.check_health()
            if unhealthy:
                print(f"[ALARM] Unhealthy agents detected: {unhealthy}")
                # Trigger task reassignment if TaskManager is present
                if self.task_manager:
                    for agent_name in unhealthy:
                        reassigned_count = self.task_manager.reassign_tasks_for_agent(agent_name)
                        if reassigned_count > 0:
                            print(f"[Heartbeat] Reassigned {reassigned_count} tasks from offline agent: {agent_name}")
            time.sleep(self.interval)

    def stop(self):
        self.running = False
        if self._thread:
            self._thread.join()

if __name__ == "__main__":
    hb = HeartbeatManager(interval=1.0)
    hb.register_agent("Agent-001")
    hb.start()
    time.sleep(0.5)
    hb.pulse("Agent-001")
    time.sleep(1.5)
    print("Health check completed.")
    hb.stop()
