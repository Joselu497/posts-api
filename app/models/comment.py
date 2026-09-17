from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.post import Post


class Comment(Base):
    __tablename__ = "comments"

    content: Mapped[str] = mapped_column(String(255))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    post: Mapped["Post"] = relationship(back_populates="comments")