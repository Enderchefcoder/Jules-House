import re

class SwarmFirewall:
    """
    Monitors the MessageBus for suspicious patterns, injection attempts,
    or malformed packets to ensure swarm integrity.
    """
    def __init__(self):
        self.blocked_senders = set()
        self.security_logs = []
        # Suspicious patterns: SQL injection-like, shell metacharacters, or anomalous coordinate ranges
        self.danger_patterns = [
            r"([;'\"]|--)",      # Basic injection
            r"(\.\./|\.\.\\)",   # Path traversal
            r"(rm\s+-rf|sudo)",  # Malicious commands
            r"(\d{5,})"          # Anomalous large numbers (overflow attempts)
        ]

    def validate_message(self, sender, content, msg_type):
        """Checks if a message is safe to process."""
        if sender in self.blocked_senders:
            return False

        str_content = str(content)
        for pattern in self.danger_patterns:
            if re.search(pattern, str_content):
                self.log_threat(sender, "Malicious Pattern Detected", content)
                self.blocked_senders.add(sender)
                return False

        # Type-specific validation
        if msg_type == "resource_discovery":
            # Content should be (item, (x, y, z))
            if not isinstance(content, (list, tuple)) or len(content) != 2:
                self.log_threat(sender, "Malformed Resource Packet", content)
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
