from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.core.config import settings

DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/db_posts_dev"

engine = create_async_engine(settings.database_url, echo=True)

async_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with async_session() as session:
        yield session