from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin
from app.database.session import get_db
from app.models.office_map_settings import OfficeMapSettings
from app.schemas.office_map_settings import OfficeMapSettingsIn, OfficeMapSettingsRead


router = APIRouter(prefix="/office-map-settings", tags=["office-map-settings"])


def get_singleton_settings(db: Session) -> OfficeMapSettings:
    settings = db.query(OfficeMapSettings).first()
    if settings is not None:
        return settings

    settings = OfficeMapSettings(office_map_image_url=None)
    db.add(settings)
    db.commit()
    db.refresh(settings)
    return settings


@router.get("", response_model=OfficeMapSettingsRead)
def read_office_map_settings(db: Session = Depends(get_db)):
    settings = db.query(OfficeMapSettings).first()
    return OfficeMapSettingsRead(office_map_image_url=settings.office_map_image_url if settings else None)


@router.put("", response_model=OfficeMapSettingsRead)
def update_office_map_settings(
    settings_in: OfficeMapSettingsIn,
    db: Session = Depends(get_db),
    _: None = Depends(get_current_admin),
):
    settings = get_singleton_settings(db)
    settings.office_map_image_url = settings_in.office_map_image_url
    db.commit()
    db.refresh(settings)
    return OfficeMapSettingsRead(office_map_image_url=settings.office_map_image_url)

