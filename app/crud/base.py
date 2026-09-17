from typing import Type

from alembic.util import status
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.base import Base

async def get(db: AsyncSession, model: Type[Base], id: int) -> Base | None:
    '''
    Retrieve a single record from the database by its primary key (id).
    
    param: db: The asynchronous database session.
    param: model: The SQLAlchemy model class to query.
    param: id: The primary key of the record to retrieve.
    return: The record if found, otherwise None.
    '''
    result = await db.execute(select(model).where(model.id == id).where(model.deleted_at == None))
    
    return result.scalar_one_or_none()

async def all(db: AsyncSession, model: Type[Base], skip: int = 0, limit: int = 10, show_deleted: bool = False) -> list[Base]:
    '''
    Retrieve all records from the database for a given model, with optional pagination.

    param: db: The asynchronous database session.
    param: model: The SQLAlchemy model class to query.
    param: skip: The number of records to skip (for pagination).
    param: limit: The maximum number of records to return (for pagination).
    return: A list of records.
    '''
    if show_deleted:
        result = await db.execute(select(model).offset(skip).limit(limit))
    else:
        result = await db.execute(select(model).offset(skip).limit(limit).where(model.deleted_at == None))
    
    return result.scalars().all()

async def delete(db: AsyncSession, model: Type[Base], id: int) -> None:
    '''
    Soft delete a record from the database by its primary key (id).

    param: db: The asynchronous database session.
    param: model: The SQLAlchemy model class to query.
    param: id: The primary key of the record to delete.
    raise: HTTPException: If the record is not found.
    '''
    obj = await get(db, model, id)

    if obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model.__name__} with id {id} not found",
        )

    obj.soft_delete()
    await db.commit()