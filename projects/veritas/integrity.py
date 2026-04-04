import hmac
import hashlib
import os

class IntegrityManager:
    """Manages the integrity and provenance of simulation artifacts."""

    def __init__(self, secret_key=None):
        self.secret_key = secret_key or os.urandom(32)

    def sign_data(self, data):
        """Signs the given data (bytes or string) using HMAC-SHA256."""
        if isinstance(data, str):
            data = data.encode('utf-8')

        signature = hmac.new(self.secret_key, data, hashlib.sha256).hexdigest()
        return signature

    def verify_data(self, data, signature):
        """Verifies the given data against the signature."""
        expected_signature = self.sign_data(data)
        return hmac.compare_digest(expected_signature, signature)

    def sign_file(self, filepath):
        """Generates a signature for a file."""
        with open(filepath, 'rb') as f:
            data = f.read()
        return self.sign_data(data)

    def verify_file(self, filepath, signature):
        """Verifies a file against its signature."""
        with open(filepath, 'rb') as f:
            data = f.read()
        return self.verify_data(data, signature)

if __name__ == "__main__":
    # Internal test
    manager = IntegrityManager(secret_key=b"test-secret")
    test_msg = "AETHER Simulation Log Step 1: Humanoid moved."
    sig = manager.sign_data(test_msg)
    print(f"Message: {test_msg}")
    print(f"Signature: {sig}")
    print(f"Verified: {manager.verify_data(test_msg, sig)}")
    print(f"Tamper test: {manager.verify_data(test_msg + ' (modified)', sig)}")
