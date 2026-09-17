from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.crud import user
from app.database import get_session
from app.core.security import generate_access_token
from app.schemas.auth import LoginResponse


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/login", response_model=LoginResponse)
async def login(username: str, password: str, db: Session = Depends(get_session)):
    '''
    Authenticate a user and return a JWT token if credentials are valid.
    :param username: The username of the user attempting to log in.
    :param password: The password provided by the user.
    :param db: The asynchronous database session.
    :return: A dictionary containing the user object, access token, and token type.
    :raise HTTPException: If the credentials are invalid.
    '''
    user_obj = await user.verify_user_credentials(db, username=username, password=password)

    if user_obj is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    jwt_token = generate_access_token(data={"sub": user_obj.username})

    return {"user": user_obj, "access_token": jwt_token, "token_type": "bearer"}