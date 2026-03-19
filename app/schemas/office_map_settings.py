from pydantic import BaseModel


class OfficeMapSettingsIn(BaseModel):
    office_map_image_url: str | None = None


class OfficeMapSettingsRead(BaseModel):
    office_map_image_url: str | None = None

