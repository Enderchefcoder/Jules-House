import re

class SwarmFirewall:
    """
    Monitors the MessageBus for suspicious patterns, injection attempts,
    or malformed packets to ensure swarm integrity.
    """
    def __init__(self):
        self.blocked_senders = set()
        self.security_logs = []
        self.sender_history = {} # {sender: [timestamp, ...]}
        # Suspicious patterns: SQL injection-like, shell metacharacters, or anomalous coordinate ranges
        self.danger_patterns = [
            r"([;'\"]|--)",      # Basic injection
            r"(\.\./|\.\.\\)",   # Path traversal
            r"(rm\s+-rf|sudo)",  # Malicious commands
            r"(\d{5,})"          # Anomalous large numbers (overflow attempts)
        ]

    def validate_message(self, sender, content, msg_type, governor=None):
        """Checks if a message is safe to process."""
        if sender in self.blocked_senders:
            return False

        str_content = str(content)
        for pattern in self.danger_patterns:
            if re.search(pattern, str_content):
                self.log_threat(sender, "Malicious Pattern Detected", content)
                self.blocked_senders.add(sender)
                if governor and hasattr(governor, 'quarantine_agent'):
                    governor.quarantine_agent(sender)
                return False

        # Type-specific validation
        if msg_type == "resource_discovery":
            # Content should be (item, (x, y, z))
            if not isinstance(content, (list, tuple)) or len(content) != 2:
                self.log_threat(sender, "Malformed Resource Packet", content)
                if governor and hasattr(governor, 'quarantine_agent'):
                    governor.quarantine_agent(sender)
                return False

        # Behavioral Analysis: Spam Detection
        import time
        now = time.time()
        if sender not in self.sender_history:
            self.sender_history[sender] = []
        self.sender_history[sender].append(now)

        # Keep only last 10s of history
        self.sender_history[sender] = [t for t in self.sender_history[sender] if now - t < 10]

        if len(self.sender_history[sender]) > 5: # Threshold: 5 msgs / 10s
            self.log_threat(sender, "Spamming Detected", content)
            self.blocked_senders.add(sender)
            if governor and hasattr(governor, 'quarantine_agent'):
                governor.quarantine_agent(sender)
            return False

        return True

    def log_threat(self, sender, threat_type, content):
        entry = {
            "sender": sender,
            "type": threat_type,
            "content_snippet": str(content)[:50],
            "timestamp": "2026-04-07"
        }
        self.security_logs.append(entry)
        print(f"[AEGIS-FIREWALL] ALERT: {threat_type} from {sender}!")

if __name__ == "__main__":
    print("Project AEGIS: SwarmFirewall module loaded.")
