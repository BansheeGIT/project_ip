from __future__ import annotations

import base64
import json
import os
from dataclasses import dataclass
from typing import Any

try:
    from cryptography.fernet import Fernet, InvalidToken
except ImportError:  # pragma: no cover - dependency may be absent in CI/runtime
    Fernet = None  # type: ignore[assignment]

    class InvalidToken(Exception):
        pass


class SecurityError(Exception):
    """Raised when MQTT payload encryption/decryption fails."""



def is_fernet_available() -> bool:
    return Fernet is not None


@dataclass
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

    key = os.getenv(env_var)
    if not key:
        if not allow_generate:
            return None
        key_bytes = FernetSecurity.generate_key()
        os.environ[env_var] = key_bytes.decode("utf-8")
        return FernetSecurity(key=key_bytes)

    return FernetSecurity(key=FernetSecurity.normalize_key(key))
