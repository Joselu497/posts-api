from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.post import Post


class User(Base):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    posts: Mapped[list["Post"]] = relationship(back_populates="users", cascade="all, delete-orphan")