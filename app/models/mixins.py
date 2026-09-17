from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


class SoftDeleteMixin:
    '''
    Provides soft delete functionality for SQLAlchemy models. It adds a deleted_at column to the model, 
    which is set to the current timestamp when the record is soft deleted
    '''
    deleted_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
        index=True,
    )

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    def soft_delete(self) -> None:
        self.deleted_at = func.now()

    def restore(self) -> None:
        self.deleted_at = None

class TimestampMixin:
    '''
    Provides automatic timestamping for SQLAlchemy models. It adds created_at and updated_at columns to the model, 
    which are automatically set to the current timestamp when a record is created or updated, respectively.
    '''
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        index=True,
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        index=True,
    )