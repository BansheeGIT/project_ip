import base64
import json
import os
from dataclasses import dataclass

try:
    from cryptography.fernet import Fernet, InvalidToken
except ImportError:
    # Let the rest of the project run even if cryptography is missing.
    Fernet = None
    # This fake error keeps the code shape the same.
    class InvalidToken(Exception): pass


# Use this for security-related problems.
class SecurityError(Exception):
    pass


# Tell the app if Fernet support is ready.
def is_fernet_available() -> bool:
    return Fernet is not None


@dataclass
# This wraps Fernet so the other code stays simple.
class FernetSecurity:
    key: bytes

    # Build the Fernet helper once after init.
    def __post_init__(self):
        # Reuse this helper for every message later on.
        if not is_fernet_available():
            raise SecurityError("Install cryptography to use Fernet: pip install cryptography")
        self._fernet = Fernet(self.key)

    @staticmethod
    # Make a new random Fernet key.
    def generate_key() -> bytes:
        if not is_fernet_available():
            raise SecurityError("Cannot generate key without cryptography")
        return Fernet.generate_key()

    @staticmethod
    # This key should look like a real Fernet key.
    def normalize_key(key) -> bytes:
        # Fernet keys must decode to 32 raw bytes.
        key_bytes = key.encode("utf-8") if isinstance(key, str) else key
        try:
            if len(base64.urlsafe_b64decode(key_bytes)) != 32:
                raise SecurityError("Invalid Fernet key length")
        except Exception:
            raise SecurityError("Invalid Fernet key encoding")
        return key_bytes

    # Encrypt one payload dict.
    def encrypt_payload(self, payload: dict) -> bytes:
        plain = json.dumps(payload).encode("utf-8")
        return self._fernet.encrypt(plain)

    # Decrypt one payload dict.
    def decrypt_payload(self, token: bytes) -> dict:
        try:
            plain = self._fernet.decrypt(token)
            data = json.loads(plain.decode("utf-8"))
            if not isinstance(data, dict):
                raise ValueError
            return data
        except (InvalidToken, Exception):
            raise SecurityError("Failed to decrypt or decode MQTT payload")


# Build a security helper from the environment if possible.
def build_fernet_security_from_env(env_var="MQTT_FERNET_KEY", allow_generate=True):
    if not is_fernet_available():
        return None

    # Reuse the env key if it exists. If not, make one for this run.
    key = os.getenv(env_var)
    if not key:
        if not allow_generate:
            return None
        key_bytes = FernetSecurity.generate_key()
        os.environ[env_var] = key_bytes.decode("utf-8")
        return FernetSecurity(key=key_bytes)

    return FernetSecurity(key=FernetSecurity.normalize_key(key))
