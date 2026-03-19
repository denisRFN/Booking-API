from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database.session import Base


class DeskLayout(Base):
    __tablename__ = "desk_layouts"

    desk_id: Mapped[int] = mapped_column(
        ForeignKey("desks.id", ondelete="CASCADE"),
        primary_key=True,
    )
    rotation_deg: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

