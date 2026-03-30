<<<<<<< HEAD
from __future__ import annotations

=======
>>>>>>> master
import base64
import json
import os
from dataclasses import dataclass
<<<<<<< HEAD
from typing import Any

try:
    from cryptography.fernet import Fernet, InvalidToken
except ImportError:  # pragma: no cover - dependency may be absent in CI/runtime
    Fernet = None  # type: ignore[assignment]

    class InvalidToken(Exception):
        pass


class SecurityError(Exception):
    """Raised when MQTT payload encryption/decryption fails."""



=======

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
>>>>>>> master
def is_fernet_available() -> bool:
    return Fernet is not None


@dataclass
<<<<<<< HEAD
class FernetSecurity:
    """Encrypt/decrypt MQTT payload dictionaries with Fernet."""

    key: bytes

    def __post_init__(self) -> None:
        if not is_fernet_available():
            raise SecurityError(
                "cryptography is not installed; Fernet security is unavailable. "
                "Install with: py -m pip install cryptography"
            )
        self._fernet = Fernet(self.key)

    @staticmethod
    def generate_key() -> bytes:
        if not is_fernet_available():
            raise SecurityError("Cannot generate Fernet key without cryptography installed")
        return Fernet.generate_key()

    @staticmethod
    def normalize_key(key: str | bytes) -> bytes:
        key_bytes = key.encode("utf-8") if isinstance(key, str) else key
        # Validate base64-url format expected by Fernet (32-byte key when decoded).
        try:
            decoded = base64.urlsafe_b64decode(key_bytes)
        except Exception as exc:  # pragma: no cover - defensive
            raise SecurityError("Invalid Fernet key encoding") from exc
        if len(decoded) != 32:
            raise SecurityError("Invalid Fernet key length")
        return key_bytes

    def encrypt_payload(self, payload: dict[str, Any]) -> bytes:
        plain = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        return self._fernet.encrypt(plain)

    def decrypt_payload(self, token: bytes) -> dict[str, Any]:
        try:
            plain = self._fernet.decrypt(token)
        except InvalidToken as exc:
            raise SecurityError("Failed to decrypt MQTT payload") from exc
        try:
            data = json.loads(plain.decode("utf-8"))
        except Exception as exc:  # pragma: no cover - defensive
            raise SecurityError("Decrypted MQTT payload is not valid JSON") from exc
        if not isinstance(data, dict):
            raise SecurityError("Decrypted MQTT payload must be an object")
        return data



def build_fernet_security_from_env(
    env_var: str = "MQTT_FERNET_KEY",
    allow_generate: bool = True,
) -> FernetSecurity | None:
    """Build Fernet security from env key; can auto-generate key for local runs."""
    if not is_fernet_available():
        return None

=======
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
>>>>>>> master
    key = os.getenv(env_var)
    if not key:
        if not allow_generate:
            return None
        key_bytes = FernetSecurity.generate_key()
        os.environ[env_var] = key_bytes.decode("utf-8")
        return FernetSecurity(key=key_bytes)

    return FernetSecurity(key=FernetSecurity.normalize_key(key))
