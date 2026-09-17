from datetime import timedelta, datetime, timezone

import jwt

from app.core.config import settings
from app.crud import user

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

def verify_access_token(token: str) -> dict:
    '''
    Verifies the given JWT access token and returns the decoded data if valid.
    Raises an exception if the token is invalid or expired.
    '''
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")
    