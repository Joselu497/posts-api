from datetime import timedelta, datetime, timezone

import jwt

from app.core.config import settings

ALGORITHM = "HS256"

def generate_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    '''
    Generates a JWT access token with the given data and expiration time.
    The token is signed using the secret key and the specified algorithm.
    '''
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)
    
    return encoded_jwt