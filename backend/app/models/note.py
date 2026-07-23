from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin
if TYPE_CHECKING:
    from app.models.user import User


class Note(TimestampMixin, Base):
    __tablename__ = "notes"

    title: Mapped[str] = mapped_column(nullable=False)

    content: Mapped[str] = mapped_column(Text)

    owner_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    owner: Mapped["User"] = relationship(back_populates="notes")