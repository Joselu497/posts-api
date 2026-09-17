import bcrypt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas import CreateUser,UpdateUser

async def create_user(db: AsyncSession, payload: CreateUser) -> User:
    '''
    Create a new user in the database.
    :param db: The asynchronous database session.
    :param payload: The data for the new user, as a CreateUser schema.
    :return: The newly created User object.
    '''
    user = User(
        email=payload.email,
        username=payload.username,
        password=bcrypt.hashpw(payload.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def update_user(
    db: AsyncSession,
    user_obj: User,
    user_data: UpdateUser,
) -> User:
    '''
    Update an existing user in the database.
    :param db: The asynchronous database session.
    :param user_obj: The existing User object to update.
    :param user_data: The data to update the user with, as an UpdateUser schema.
    :return: The updated User object.
    '''
    data = user_data.model_dump(exclude_unset=True)

    if "password" in data:
        hashed = bcrypt.hashpw(
            data.pop("password").encode("utf-8"),
            bcrypt.gensalt(),
        )
        data["password"] = hashed.decode("utf-8")
    
    for key, value in data.items():
        setattr(user_obj, key, value)

    await db.commit()
    await db.refresh(user_obj)
    return user_obj