from datetime import timedelta

from app.core import security
from app.core.config import settings


def test_password_hash_and_verify():
    password = "correct-horse-battery-staple"
    hashed = security.get_password_hash(password)

    assert hashed != password
    assert security.verify_password(password, hashed)
    assert not security.verify_password("wrong-password", hashed)


def test_access_token_contains_subject_and_expiry():
    token = security.create_access_token(
        {"sub": "security@example.com"},
        expires_delta=timedelta(minutes=5),
    )

    import jwt

    payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )
    assert payload["sub"] == "security@example.com"
    assert "exp" in payload
