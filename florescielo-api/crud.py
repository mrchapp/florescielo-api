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


def device_db_store(db: Session, id: str):
    record = get_device(db, id)
    return record.store_data


def device_db_store_sky(db: Session, record: models.SkyRecord):
    db.add(record)
    db.commit()


def device_db_store_storm(db: Session, record: models.StormRecord):
    db.add(record)
    db.commit()


def device_wunderground_publish(db: Session, id: str):
    record = get_device(db, id)
    return record.wunderground_publish


def get_wunderground_station_by_device_id(db: Session, device_id: str):
    return (
        db.query(models.WundergroundDevice)
        .filter(models.WundergroundDevice.device_id == device_id.lower())
        .first()
    )


def get_wunderground_key_by_station_id(db: Session, station_id: str):
    return (
        db.query(models.WundergroundStation)
        .filter(models.WundergroundStation.station_id == station_id)
        .first()
    )


def get_wunderground_credentials(db: Session, device_id: str):
    record = get_wunderground_station_by_device_id(db, device_id.lower())
    station_key = get_wunderground_key_by_station_id(
        db, str(record.station_id)
    ).station_key
    return record.station_id, station_key
