from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import user
from app.database import get_session
from app.core.security import generate_access_token
from app.dependencies.auth import get_current_user
from app.schemas.auth import LoginResponse
from app.schemas.user import UserResponse


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/login", response_model=LoginResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    '''
    Authenticate a user and return a JWT token if credentials are valid.
    :param username: The username of the user attempting to log in.
    :param password: The password provided by the user.
    :param db: The asynchronous database session.
    :return: A dictionary containing the user object, access token, and token type.
    :raise HTTPException: If the credentials are invalid.
    '''
    user_obj = await user.verify_user_credentials(
        db, username=form_data.username, password=form_data.password
    )

    if user_obj is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    jwt_token = generate_access_token(data={"sub": user_obj.username})

    return {"access_token": jwt_token, "token_type": "bearer"}

@router.post("/register", response_model=LoginResponse)
async def register(user_data: user.CreateUser, db: AsyncSession = Depends(get_session)):
    '''
    Register a new user and return a JWT token upon successful registration.
    :param user_data: The data for the new user, as a CreateUser schema.
    :param db: The asynchronous database session.
    :return: A dictionary containing the user object, access token, and token type.
    :raise HTTPException: If the username or email is already registered.
    '''
    existing_user = await user.get_user_by_username(db, username=user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    new_user = await user.create_user(db, payload=user_data)

    jwt_token = generate_access_token(data={"sub": new_user.username})

    return {"access_token": jwt_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    '''
    Retrieve the current authenticated user's information.
    :param current_user: The current authenticated user, obtained from the JWT token.
    :return: The UserResponse object containing the user's information.
    '''
    return current_user