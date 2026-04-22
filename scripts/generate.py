import hashlib
import hmac


def sign_payload(payload: bytes, secret: str) -> str:
    """Return HMAC-SHA256 hex digest for *payload* using *secret*."""
    key = secret.encode()
    return hmac.new(key, payload, hashlib.sha256).hexdigest()


def verify_signature(payload: bytes, secret: str, signature: str) -> bool:
    expected = sign_payload(payload, secret)
    return hmac.compare_digest(expected, signature)

# updated: 2026-04-22 05:33:36
