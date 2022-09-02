from sqlalchemy import Boolean, Column, Float, String, Integer

from .database import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(String, primary_key=True, index=True)
    owner = Column(String)
    type = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    altitude = Column(Float)
    store_data = Column(Boolean)


class SkyRecord(Base):
    __tablename__ = "skyrecords"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, index=True)
    timestamp = Column(Integer, index=True)
    temperature = Column(Float)
    humidity = Column(Float)
    voltage = Column(Integer)
    uvindex = Column(Integer)
    luminance = Column(Integer)
    rain = Column(Boolean)
    pressure = Column(Integer)
    charger_status = Column(Boolean)


class StormRecord(Base):
    __tablename__ = "stormrecords"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, index=True)
    timestamp = Column(Integer, index=True)
    rain = Column(Integer)
    wind_speed = Column(Integer)
    wind_direction = Column(Integer)
    voltage = Column(Integer)
    uv = Column(Integer)
    debug_info = Column(String)
