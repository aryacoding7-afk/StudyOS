from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin


class File(TimestampMixin, Base):
    __tablename__ = "files"

    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    filepath: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    owner_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    owner = relationship(
        "User",
        back_populates="files",
    )

    document = relationship(
        "Document",
        back_populates="file",
        uselist=False,
        cascade="all, delete-orphan",
    )