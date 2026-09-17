from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.post import Post


class Tag(Base):
    __tablename__ = 'tags'

    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    posts: Mapped[list["Post"]] = relationship(secondary="post_tags", back_populates="tags")