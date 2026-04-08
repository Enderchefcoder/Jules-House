class RelayBeacon:
    """
    Project ORION: Long-Range Communication Relay Beacon.
    Extends the effective communication range for agents in the AETHER swarm.
    """
    def __init__(self, position, range_boost=15):
        self.position = position
        self.range_boost = range_boost
        self.is_active = True

    def toggle(self):
        self.is_active = not self.is_active
        print(f"[ORION] Relay at {self.position} is now {'ACTIVE' if self.is_active else 'INACTIVE'}")

    def __repr__(self):
        return f"RelayBeacon({self.position}, Boost: {self.range_boost}, Active: {self.is_active})"
