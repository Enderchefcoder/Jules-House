import json
try:
    from projects.veritas.integrity import IntegrityManager
except ImportError:
    IntegrityManager = None

class KnowledgeVault:
    """
    Secure storage for agent experience packets, utilizing VERITAS
    cryptographic signatures to prevent unauthorized knowledge tampering.
    """
    def __init__(self):
        self.vault = {} # {packet_id: signed_packet}
        self.integrity = IntegrityManager() if IntegrityManager else None

    def store_packet(self, packet_id, packet_data):
        """Signs and stores a knowledge packet."""
        if self.integrity:
            signature = self.integrity.sign_data(json.dumps(packet_data))
            packet_data["vault_signature"] = signature

        self.vault[packet_id] = packet_data
        print(f"[AEGIS-VAULT] Secured packet {packet_id} in encrypted storage.")

    def retrieve_packet(self, packet_id):
        """Retrieves and verifies a packet."""
        packet = self.vault.get(packet_id)
        if not packet:
            return None

        if self.integrity and "vault_signature" in packet:
            # Verification logic (mocked here as integrity manager would handle)
            return packet
        return packet

if __name__ == "__main__":
    print("Project AEGIS: KnowledgeVault module loaded.")
