"""Authentication helper utilities."""
import hashlib
import hmac
import secrets
import base64
from datetime import datetime, timedelta


def generate_token(length: int = 32) -> str:
    """Generate a cryptographically secure random token."""
    return secrets.token_urlsafe(length)


def sign_request(payload: str, secret: str) -> str:
    """Sign a request payload with HMAC-SHA256."""
    return hmac.new(
        secret.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()


def verify_signature(payload: str, secret: str, signature: str) -> bool:
    """Verify HMAC-SHA256 signature."""
    expected = sign_request(payload, secret)
    return hmac.compare_digest(expected, signature)


def encode_basic_auth(username: str, password: str) -> str:
    """Encode credentials for HTTP Basic Auth."""
    credentials = f'{username}:{password}'
    encoded = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
    return f'Basic {encoded}'
