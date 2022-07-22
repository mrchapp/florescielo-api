from sqlalchemy.orm import Session

from . import models


def get_device(db: Session, id: str):
    return db.query(models.Device).filter(models.Device.id == id.lower()).first()


def get_device_location(db: Session, id: str):
    record = db.query(models.Device).filter(models.Device.id == id.lower()).first()
    return record.latitude, record.longitude


def get_device_type(db: Session, id: str):
    record = db.query(models.Device).filter(models.Device.id == id.lower()).first()
    return record.type
