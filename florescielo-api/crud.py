import datetime

from sqlalchemy.orm import Session

from . import models, schemas


def get_device_location(db: Session, id: str):
    id_lower = id.lower()
    return (
        db.query(models.DeviceLocation)
        .filter(models.DeviceLocation.id == id_lower)
        .first()
    )
