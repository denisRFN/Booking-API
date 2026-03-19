from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.session import Base


class OfficeMapSettings(Base):
    __tablename__ = "office_map_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    office_map_image_url: Mapped[str | None] = mapped_column(String, nullable=True)

