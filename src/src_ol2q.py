import hashlib
import hmac


def sign_payload(payload: bytes, secret: str) -> str:
    key = secret.encode()
    return hmac.new(key, payload, hashlib.sha256).hexdigest()


def verify_signature(payload: bytes, secret: str, signature: str) -> bool:
    expected = sign_payload(payload, secret)
    return hmac.compare_digest(expected, signature)

# 2026-04-28 04:34:49
