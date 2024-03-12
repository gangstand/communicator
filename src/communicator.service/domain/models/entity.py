import uuid
from datetime import datetime
from uuid import UUID

from sqlalchemy import TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure import Base


class Entity(Base):
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    is_removing: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )

    @property
    def identity(self) -> UUID:
        """Get the entity's UUID."""
        return self.id

    def __str__(self) -> str:
        """Return a string representation of the object's UUID."""
        return str(self.id)
